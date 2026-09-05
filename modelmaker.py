"""program to make model for user as per his requirements"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb
import os
import html
from sklearn.model_selection import train_test_split
import streamlit as st
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
data = None

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Space+Mono:wght@400;700&display=swap');

    :root {
        --mm-ink: #F5F1FF;
        --mm-soft: #B8B2D6;
        --mm-faint: #827C9F;
        --mm-paper: #050612;
        --mm-card: rgba(15, 17, 40, 0.88);
        --mm-line: rgba(151, 126, 255, 0.24);
        --mm-accent: #8C7BFF;
        --mm-cyan: #4DE8FF;
        --mm-pink: #FF69D4;
    }

    [data-testid="stAppViewContainer"] {
        color: var(--mm-ink) !important;
        font-family: 'Space Grotesk', sans-serif !important;
        background:
            radial-gradient(circle at 12% 6%, rgba(79, 91, 255, 0.2), transparent 28rem),
            radial-gradient(circle at 88% 22%, rgba(255, 105, 212, 0.11), transparent 25rem),
            radial-gradient(circle at 62% 90%, rgba(77, 232, 255, 0.09), transparent 28rem),
            linear-gradient(145deg, #050612 0%, #090A1D 48%, #050612 100%) !important;
    }

    [data-testid="stAppViewContainer"]::before {
        content: "";
        position: fixed;
        inset: 0;
        pointer-events: none;
        opacity: 0.42;
        background-image: radial-gradient(circle, rgba(255,255,255,0.8) 0 1px, transparent 1.3px);
        background-size: 150px 150px;
        animation: mm-stars 45s linear infinite;
    }

    @keyframes mm-stars {
        to { background-position: 0 150px; }
    }

    [data-testid="stMainBlockContainer"] {
        max-width: 1080px;
        padding-top: 2.25rem;
        padding-bottom: 4rem;
    }

    [data-testid="stMarkdownContainer"],
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] li {
        color: var(--mm-ink);
    }

    [data-testid="stMarkdownContainer"] h1,
    [data-testid="stMarkdownContainer"] h2,
    [data-testid="stMarkdownContainer"] h3 {
        font-family: 'Space Grotesk', sans-serif !important;
        color: var(--mm-ink) !important;
        letter-spacing: 0;
    }

    [data-testid="stCaptionContainer"],
    [data-testid="stWidgetLabel"] p {
        color: var(--mm-soft) !important;
        font-family: 'Space Mono', monospace !important;
        letter-spacing: 0.04em;
    }

    [data-testid="stHeader"] {
        background: rgba(5, 6, 18, 0.72) !important;
        border-bottom: 1px solid var(--mm-line);
        backdrop-filter: blur(14px);
    }

    .mm-hero {
        background: linear-gradient(125deg, rgba(20, 22, 53, 0.96), rgba(10, 11, 30, 0.92));
        border: 1px solid rgba(151, 126, 255, 0.34);
        border-top: 2px solid var(--mm-accent);
        border-radius: 14px;
        padding: 2rem 2.1rem 1.55rem;
        margin-bottom: 1.6rem;
        box-shadow: 0 0 24px rgba(140, 123, 255, 0.18), inset 0 1px 0 rgba(255,255,255,0.05);
        animation: mm-rise 0.45s ease both;
    }

    @keyframes mm-rise {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .mm-eyebrow, .mm-label {
        color: var(--mm-cyan);
        font-family: 'Space Mono', monospace;
        font-size: 0.68rem;
        letter-spacing: 0.16em;
        text-transform: uppercase;
    }

    .mm-title {
        margin: 0.55rem 0 0.45rem;
        color: var(--mm-ink);
        font-size: clamp(2.2rem, 6vw, 3.4rem);
        font-weight: 700;
        line-height: 1.05;
    }

    .mm-subtitle {
        max-width: 58ch;
        color: var(--mm-soft);
        line-height: 1.65;
        margin-bottom: 1.3rem;
    }

    .mm-fields {
        display: flex;
        flex-wrap: wrap;
        gap: 1rem 2.5rem;
        border-top: 1px solid var(--mm-line);
        padding-top: 1rem;
    }

    .mm-value {
        display: block;
        color: var(--mm-ink);
        font-family: 'Space Mono', monospace;
        font-size: 0.84rem;
        font-weight: 700;
        margin-top: 0.25rem;
    }

    [data-testid="stFileUploaderDropzone"],
    [data-testid="stSelectbox"] div[data-baseweb="select"] > div,
    [data-testid="stNumberInput"] input {
        background: rgba(10, 11, 30, 0.88) !important;
        border: 1px solid var(--mm-line) !important;
        border-radius: 8px !important;
        color: var(--mm-ink) !important;
    }

    [data-testid="stFileUploaderDropzone"] {
        border-style: dashed !important;
        background: linear-gradient(135deg, rgba(140,123,255,0.06), rgba(77,232,255,0.03)), rgba(10, 11, 30, 0.82) !important;
    }

    [data-testid="stBaseButton-primary"], [data-testid="stBaseButton-secondary"] {
        border-radius: 8px !important;
        font-family: 'Space Mono', monospace !important;
        font-size: 0.73rem !important;
        letter-spacing: 0.08em;
        text-transform: uppercase;
    }

    [data-testid="stBaseButton-primary"] {
        background: linear-gradient(100deg, #6658E8, var(--mm-accent)) !important;
        border-color: var(--mm-accent) !important;
        color: #FFFFFF !important;
        box-shadow: 0 0 16px rgba(140, 123, 255, 0.18);
    }

    [data-testid="stBaseButton-secondary"] {
        background: rgba(15, 17, 40, 0.78) !important;
        border: 1px solid var(--mm-line) !important;
        color: var(--mm-ink) !important;
    }

    [data-testid="stAlert"] {
        border: 1px solid var(--mm-line) !important;
        border-radius: 9px !important;
        background: rgba(15, 17, 40, 0.9) !important;
    }

    [data-testid="stDataFrame"] {
        border: 1px solid var(--mm-line);
        border-radius: 10px;
        overflow: hidden;
    }

    :root {
        --mm-ink: #E8EEF5;
        --mm-soft: #9BA9B8;
        --mm-faint: #687584;
        --mm-paper: #020407;
        --mm-card: rgba(9, 13, 18, 0.96);
        --mm-line: rgba(133, 157, 181, 0.2);
        --mm-accent: #5B8DEF;
        --mm-cyan: #65D9D2;
        --mm-pink: #E38ABF;
    }

    [data-testid="stAppViewContainer"] {
        background: linear-gradient(145deg, #020407 0%, #080C11 52%, #020407 100%) !important;
    }

    [data-testid="stAppViewContainer"]::before {
        opacity: 0.16;
    }

    [data-testid="stHeader"] {
        background: rgba(2, 4, 7, 0.9) !important;
        border-bottom-color: rgba(133, 157, 181, 0.16);
    }

    .mm-hero {
        background: linear-gradient(135deg, rgba(12, 18, 26, 0.98), rgba(6, 10, 15, 0.98));
        border-color: rgba(133, 157, 181, 0.22);
        border-top-color: var(--mm-cyan);
        box-shadow: 0 16px 40px rgba(0, 0, 0, 0.28), inset 0 1px 0 rgba(255,255,255,0.04);
    }

    [data-testid="stFileUploaderDropzone"],
    [data-testid="stSelectbox"] div[data-baseweb="select"] > div,
    [data-testid="stNumberInput"] input {
        background: #080D12 !important;
        border-color: rgba(133, 157, 181, 0.22) !important;
    }

    [data-testid="stBaseButton-primary"] {
        background: #3F6FC7 !important;
        border-color: #5B8DEF !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="mm-hero">
      <div class="mm-eyebrow">Model Lab · supervised learning workspace</div>
      <div class="mm-title">Model Maker</div>
      <div class="mm-subtitle">
        Turn a clean CSV into a tested prediction model with transparent feature selection and a live input check.
      </div>
      <div class="mm-fields">
        <div><span class="mm-label">Workflow</span><span class="mm-value">Train · inspect · predict</span></div>
        <div><span class="mm-label">Inputs</span><span class="mm-value">CSV data</span></div>
        <div><span class="mm-label">Output</span><span class="mm-value">Scikit-learn model</span></div>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.subheader("Upload your dataset")
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])
if uploaded_file is not None:
    Data = pd.read_csv(uploaded_file)
    data = Data.copy()
    
else:
    st.info("Please upload a CSV file to continue.")
    st.stop()
    raise SystemExit



st.table(data.head(50))

# finding and replacing the null values
null_columns = data.isnull().sum().index[data.isnull().sum()>0].tolist()

for fn in null_columns:
    if pd.api.types.is_numeric_dtype(data[fn]):
        data[fn] = data[fn].fillna(data.loc[data[fn]!=np.nan,fn].mean())
    
    else:
        mostrepeted = data[fn].value_counts().idxmax()
        data[data[fn]==np.nan][fn] = mostrepeted
        
# droping duplicate rows if any
if data.duplicated().sum() >0:
    data = data.drop_duplicates()
    


st.write("choose the target variable")

target_variable = st.selectbox("Select the target variable:", data.columns)

y = data[target_variable].copy()
valid_target_rows = y.notna()
if not valid_target_rows.any():
    st.error("The selected target variable has no usable values.")
    st.stop()

data = data.loc[valid_target_rows].copy()
y = y.loc[valid_target_rows]
is_classification = (
    not pd.api.types.is_numeric_dtype(y) or y.nunique() <= 2
)

no_of_features = st.slider("Select the number of features to use for the model:", min_value=1, max_value=len(data.columns)-1, value=3)

features = st.multiselect("Select the features to use for the model:", data.columns.drop(target_variable), default=data.columns.drop(target_variable)[:no_of_features])

x = data[features]

numeric_columns = x.select_dtypes(include=np.number).columns.tolist()

categorical_columns = x.select_dtypes(exclude=np.number).columns.tolist()
max_categories = 100
high_cardinality_columns = [
    column for column in categorical_columns
    if x[column].nunique(dropna=True) > max_categories
]

if high_cardinality_columns:
    x = x.drop(columns=high_cardinality_columns)
    categorical_columns = [
        column for column in categorical_columns
        if column not in high_cardinality_columns
    ]
    st.warning(
        "Skipped high-cardinality feature(s): "
        + ", ".join(high_cardinality_columns)
    )

if x.shape[1] == 0:
    st.error("Select at least one numeric or low-cardinality feature.")
    st.stop()

features = x.columns.tolist()
numeric_columns = x.select_dtypes(include=np.number).columns.tolist()
for column in numeric_columns:
    x[column] = x[column].fillna(x[column].median())

x = pd.get_dummies(x, columns=categorical_columns, drop_first=True)

x[numeric_columns] = scaler.fit_transform(x[numeric_columns])
st.write("number of unique values in target variable:", y.nunique())
if y.nunique() > 2:
    st.write("The target variable is continuous using the regression method")
else:
    st.write("The target variable is binary using the classification method")
    st.write("Unique values are ", y.unique())
from sklearn.model_selection import train_test_split

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

Model = None

if is_classification:
    st.write("The target variable is binary using the classification method")
    
    method = st.select_slider("Select the classification method:", options=["Logistic Regression", "Random Forest Classifier", "Support Vector Classifier", "K-Nearest Neighbors Classifier", "Decision Tree Classifier"])
    
    if method == "Logistic Regression":
        from sklearn.linear_model import LogisticRegression
        model = LogisticRegression()
        model.fit(x_train, y_train)
        st.write("Model trained successfully using Logistic Regression.")
        st.write("Model accuracy on training data: {:.2f}%".format(model.score(x_test, y_test) * 100))
        Model = model
    elif method == "Random Forest Classifier":
        from sklearn.ensemble import RandomForestClassifier
        model = RandomForestClassifier()
        model.fit(x_train, y_train)
        st.write("Model trained successfully using Random Forest Classifier.")
        st.write("Model accuracy on training data: {:.2f}%".format(model.score(x_test, y_test) * 100))
        Model = model
    elif method == "Support Vector Classifier":
        from sklearn.svm import SVC
        model = SVC()
        model.fit(x_train, y_train)
        st.write("Model trained successfully using Support Vector Classifier.")
        st.write("Model accuracy on training data: {:.2f}%".format(model.score(x_test, y_test) * 100))
        Model = model
    elif method == "K-Nearest Neighbors Classifier":
        from sklearn.neighbors import KNeighborsClassifier
        model = KNeighborsClassifier()
        model.fit(x_train, y_train)
        st.write("Model trained successfully using K-Nearest Neighbors Classifier.")
        st.write("Model accuracy on training data: {:.2f}%".format(model.score(x_test, y_test) * 100))
        Model = model
    elif method == "Decision Tree Classifier":
        from sklearn.tree import DecisionTreeClassifier
        model = DecisionTreeClassifier()
        model.fit(x_train, y_train)
        st.write("Model trained successfully using Decision Tree Classifier.")
        st.write("Model accuracy on training data: {:.2f}%".format(model.score(x_test, y_test) * 100))
        Model = model
    else:   
        st.write("Invalid method selected.")
else:
    st.write("The target variable is continuous using the regression method")
    
    method = st.select_slider("Select the regression method:", options=["Linear Regression", "Random Forest Regressor", "Support Vector Regressor", "K-Nearest Neighbors Regressor", "Decision Tree Regressor"])
    
    if method == "Linear Regression":
        from sklearn.linear_model import LinearRegression
        model = LinearRegression()
        model.fit(x_train, y_train)
        st.write("Model trained successfully using Linear Regression.")
        score = model.score(x_test, y_test)
        st.write(f"Model R² on test data: {score:.3f}")
        Model = model
    elif method == "Random Forest Regressor":
        from sklearn.ensemble import RandomForestRegressor
        model = RandomForestRegressor()
        model.fit(x_train, y_train)
        st.write("Model trained successfully using Random Forest Regressor.")
        score = model.score(x_test, y_test)
        st.write(f"Model R² on test data: {score:.3f}")
        Model = model
    elif method == "Support Vector Regressor":
        from sklearn.svm import SVR
        model = SVR()
        model.fit(x_train, y_train)
        st.write("Model trained successfully using Support Vector Regressor.")
        score = model.score(x_test, y_test)
        st.write(f"Model R² on test data: {score:.3f}")
        Model = model
    elif method == "K-Nearest Neighbors Regressor":
        from sklearn.neighbors import KNeighborsRegressor
        model = KNeighborsRegressor()
        model.fit(x_train, y_train)
        st.write("Model trained successfully using K-Nearest Neighbors Regressor.")
        score = model.score(x_test, y_test)
        st.write(f"Model R² on test data: {score:.3f}")
        Model = model
    elif method == "Decision Tree Regressor":
        from sklearn.tree import DecisionTreeRegressor
        model = DecisionTreeRegressor()
        model.fit(x_train, y_train)
        st.write("Model trained successfully using Decision Tree Regressor.")
        score = model.score(x_test, y_test)
        st.write(f"Model R² on test data: {score:.3f}")
        Model = model
    else:
        st.write("Invalid method selected.")



    
btn = st.button("Save Model")

if btn:
    import joblib
    joblib.dump(Model,"model.pkl")
    joblib.dump(scaler,"scaler.pkl")
    st.write("Model saved successfully as model.pkl and scaler saved as scaler.pkl")


if "show_checker" not in st.session_state:
    st.session_state.show_checker = False

if st.button("Check model"):
    st.session_state.show_checker = True

if st.session_state.show_checker and Model is not None:
    st.subheader("Test the Model with Your Own Inputs")

    with st.form("model_check_form"):
        user_inputs = {}
        for col in features:
            if col in numeric_columns:
                user_inputs[col] = st.number_input(
                    f"Enter value for {col}",
                    float(data[col].min()),
                    float(data[col].max()),
                    float(data[col].mean()),
                )
            else:
                options = data[col].dropna().unique().tolist()
                user_inputs[col] = st.selectbox(f"Select value for {col}", options)

        predict_button = st.form_submit_button("Predict")

    if predict_button:
        input_df = pd.DataFrame([user_inputs])
        input_df = pd.get_dummies(
            input_df, columns=categorical_columns, drop_first=True
        )
        input_df = input_df.reindex(columns=x.columns, fill_value=0)
        input_df[numeric_columns] = scaler.transform(input_df[numeric_columns])
        prediction = Model.predict(input_df)[0]

        if is_classification:
            st.write(f"Predicted class: {prediction}")
        else:
            st.write(f"Predicted value: {prediction:.2f}")




