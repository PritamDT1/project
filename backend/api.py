import os
import secrets
import sys
from pathlib import Path
from typing import Any

import pandas as pd
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, r2_score

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

app = FastAPI(title="Research Orbit API", version="1.0.0")
frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173").rstrip("/")
if not frontend_url.startswith("http"):
    frontend_url = f"https://{frontend_url}"
app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_url, "http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
models: dict[str, dict[str, Any]] = {}
GEMINI_MODELS = [
    "google_genai:gemini-3.6-flash",
    "google_genai:gemini-3.5-flash",
    "google_genai:gemini-3.5-flash-lite",
]


class AuthPayload(BaseModel):
    aadhaar: str = Field(min_length=1)
    email: str = Field(min_length=3)
    name: str = ""
    age: str = ""
    phone: str = ""


class PredictPayload(BaseModel):
    model_id: str
    values: dict[str, Any]


def database():
    import database as db
    return db


def user_response(payload: AuthPayload) -> dict[str, str]:
    return {"aadhaar": payload.aadhaar, "email": payload.email, "name": payload.name or payload.email}


def clean_model_content(content: Any) -> str | list[dict[str, Any]]:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        cleaned: list[dict[str, Any]] = []
        for block in content:
            if isinstance(block, str):
                cleaned.append({"type": "text", "text": block})
            elif isinstance(block, dict) and block.get("type") == "text" and isinstance(block.get("text"), str):
                cleaned.append({"type": "text", "text": block["text"]})
            elif isinstance(block, dict) and block.get("type") in {"image", "image_url"}:
                image = {"type": block["type"]}
                for key in ("image_url", "url", "data", "mime_type"):
                    if key in block:
                        image[key] = block[key]
                cleaned.append(image)
        if cleaned:
            return cleaned
    return str(content)


@app.post("/documents/analyze")
async def analyze_documents(
    files: list[UploadFile] | None = File(None),
    query: str = Form(...),
    mode: str = Form("summarize"),
    model_name: str = Form(GEMINI_MODELS[0]),
):
    files = files or []
    if not query.strip():
        raise HTTPException(status_code=400, detail="A research prompt is required.")
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise HTTPException(status_code=503, detail="GEMINI_API_KEY is not configured.")
    if model_name not in GEMINI_MODELS:
        raise HTTPException(status_code=400, detail="Unsupported Gemini model.")
    try:
        from tempfile import TemporaryDirectory
        from reader import read_file
        from langchain.chat_models import init_chat_model

        documents = []
        with TemporaryDirectory() as temp_dir:
            for upload in files:
                path = Path(temp_dir) / (upload.filename or "document")
                path.write_bytes(await upload.read())
                documents.append(f"--- {upload.filename or 'document'} ---\n{read_file(str(path))}")
        context = "\n\n".join(documents)
        if mode == "compare" and len(files) != 2:
            raise HTTPException(status_code=400, detail="Comparison requires exactly two files.")
        instruction = {
            "summarize": "Summarize the key points and important details.",
            "compare": "Compare the two documents and identify important similarities and differences.",
            "ask": query.strip(),
        }.get(mode, query.strip())
        os.environ["GOOGLE_API_KEY"] = api_key
        model = init_chat_model(model_name, api_key=api_key)
        prompt = f"Instruction: {instruction}"
        if context:
            prompt += f"\n\nDocument context:\n{context[:120000]}"
        else:
            prompt += "\n\nNo documents were provided. Answer as a general assistant."
        response = model.invoke(prompt)
        content = clean_model_content(getattr(response, "content", response))
        return {"answer": content, "files": [f.filename for f in files]}
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Document analysis failed: {exc}")


@app.get("/health")
def health():
    return {"status": "ok", "service": "research-orbit-api"}


@app.get("/")
def root():
    return {"status": "ok", "service": "research-orbit-api", "docs": "/docs"}


@app.get("/history/{aadhaar}")
def history(aadhaar: str):
    try:
        return [
            {"question": question, "response": response, "time": time.isoformat() if time else None}
            for question, response, time in database().get_history(int(aadhaar))
        ]
    except ValueError:
        raise HTTPException(status_code=400, detail="Aadhaar card number must be numeric.")
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"History service unavailable: {exc}")


@app.post("/auth/login")
def login(payload: AuthPayload):
    try:
        if not database().authenticate(int(payload.aadhaar), payload.email.strip()):
            raise HTTPException(status_code=401, detail="Aadhaar card number and email do not match.")
        return user_response(payload)
    except ValueError:
        raise HTTPException(status_code=400, detail="Aadhaar card number must be numeric.")
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"Authentication service unavailable: {exc}")


@app.post("/auth/register")
def register(payload: AuthPayload):
    if not payload.name.strip() or not payload.age or not payload.phone.strip():
        raise HTTPException(status_code=400, detail="Name, age, and phone number are required.")
    try:
        database().create_user(int(payload.aadhaar), payload.name.strip(), int(payload.age), payload.email.strip(), payload.phone.strip())
        return user_response(payload)
    except ValueError:
        raise HTTPException(status_code=400, detail="Aadhaar and age must be numeric.")
    except Exception as exc:
        raise HTTPException(status_code=409, detail=f"Could not create account: {exc}")


@app.post("/models/train")
async def train_model(file: UploadFile = File(...), target: str = "", method: str = "Random Forest Classifier"):
    if not target:
        raise HTTPException(status_code=400, detail="Target variable is required.")
    try:
        data = pd.read_csv(file.file)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Could not read CSV: {exc}")
    if target not in data.columns:
        raise HTTPException(status_code=400, detail="Target variable was not found in the CSV.")
    data = data.dropna(subset=[target]).drop_duplicates()
    if len(data) < 4:
        raise HTTPException(status_code=400, detail="At least four valid rows are required.")
    y = data.pop(target)
    is_classification = not pd.api.types.is_numeric_dtype(y) or y.nunique() <= 2
    if is_classification:
        estimator = LogisticRegression(max_iter=1000) if method == "Logistic Regression" else RandomForestClassifier(n_estimators=150, random_state=42)
    else:
        estimator = LinearRegression() if method == "Linear Regression" else RandomForestRegressor(n_estimators=150, random_state=42)
    numeric = data.select_dtypes(include="number").columns.tolist()
    categorical = data.select_dtypes(exclude="number").columns.tolist()
    preprocess = ColumnTransformer([
        ("numeric", Pipeline([("imputer", SimpleImputer(strategy="median")), ("scale", StandardScaler())]), numeric),
        ("categorical", Pipeline([("imputer", SimpleImputer(strategy="most_frequent")), ("onehot", OneHotEncoder(handle_unknown="ignore"))]), categorical),
    ])
    pipeline = Pipeline([("preprocess", preprocess), ("model", estimator)])
    x_train, x_test, y_train, y_test = train_test_split(data, y, test_size=0.2, random_state=42)
    pipeline.fit(x_train, y_train)
    score = accuracy_score(y_test, pipeline.predict(x_test)) if is_classification else r2_score(y_test, pipeline.predict(x_test))
    model_id = secrets.token_urlsafe(12)
    models[model_id] = {"pipeline": pipeline, "classification": is_classification, "classes": y.drop_duplicates().tolist()}
    return {"model_id": model_id, "classification": is_classification, "score": float(score), "features": data.columns.tolist(), "classes": models[model_id]["classes"] if is_classification else []}


@app.post("/models/predict")
def predict(payload: PredictPayload):
    entry = models.get(payload.model_id)
    if not entry:
        raise HTTPException(status_code=404, detail="Model not found. Train it again.")
    try:
        result = entry["pipeline"].predict(pd.DataFrame([payload.values]))[0]
        return {"prediction": result.item() if hasattr(result, "item") else result, "classification": entry["classification"]}
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Prediction failed: {exc}")
