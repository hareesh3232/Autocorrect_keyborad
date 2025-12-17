from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from fastapi.middleware.cors import CORSMiddleware
from .suggestion import SuggestionEngine

app = FastAPI(title="Autocorrect Keyboard API")

# Allow CORS for local frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global engine instance
engine = None

class SuggestRequest(BaseModel):
    text: str

@app.on_event("startup")
def load_engine():
    global engine
    # Assume model is in project/models/ngram_counts.pkl
    # Adjust path relative to where uvicorn is run (usually root of repo)
    model_path = os.path.join("project", "models", "ngram_counts.pkl")
    engine = SuggestionEngine(model_path)

@app.post("/suggest")
def suggest(request: SuggestRequest):
    if not engine:
        raise HTTPException(status_code=500, detail="Engine not initialized")
    
    results = engine.get_suggestions(request.text)
    return results

@app.get("/health")
def health():
    return {"status": "ok", "model_loaded": engine is not None}

# Serve static files (Frontend)
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Mount the 'app' directory as static files
# Use absolute path relative to this file (project/src/api.py)
# project/app is ../app relative to project/src
import pathlib

current_file_path = pathlib.Path(__file__).parent.resolve()
project_root = current_file_path.parent # project/
static_dir = project_root / "app"

if static_dir.exists():
    app.mount("/", StaticFiles(directory=str(static_dir), html=True), name="static")
    print(f"Serving static files from: {static_dir}")
else:
    print(f"Warning: Frontend directory '{static_dir}' not found. UI will not be served.")
