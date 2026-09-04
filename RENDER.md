# Render deployment

The deployment blueprint creates two services:

- `research-orbit-frontend`: Vite React static site
- `research-orbit-api`: FastAPI service for authentication and model training/prediction

## Deploy

1. Push this repository to GitHub.
2. In Render, choose **New > Blueprint** and select the repository.
3. Render reads `render.yaml` and creates both services.
4. Set `MYSQLHOST`, `MYSQLPORT`, `MYSQLUSER`, `MYSQLPASSWORD`, and `MYSQLDATABASE` for the API service.
5. Set `GEMINI_API_KEY` for the API service so document analysis can call Gemini.
6. Copy the frontend public URL into `FRONTEND_URL` if Render does not resolve the service reference automatically.

The React build uses `VITE_API_URL`, which is populated from the API service in the blueprint. For local development:

```bash
cd frontend
npm install
npm run dev
```

The API can be run locally with:

```bash
uvicorn backend.api:app --reload --port 8000
```

The model service keeps trained models in memory. Train a model again after an API restart or redeploy.

For a manually created API service, leave the root directory empty, use
`pip install -r backend/requirements.txt` as the build command, and use
`uvicorn backend.api:app --host 0.0.0.0 --port $PORT` as the start command.
