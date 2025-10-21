from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.auth import verify_token, create_access_token
from app.rag_pipeline import get_qa_pipeline
from app.url_to_txt import url_to_txt
import os
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI(title="Generative AI Docs Q&A API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods including OPTIONS
    allow_headers=["*"],
)

# Pydantic models for request bodies
class UrlConvertRequest(BaseModel):
    url: str

class AskRequest(BaseModel):
    query: str

@app.get("/")
def root():
    return {"message": "Welcome to Generative AI Q&A API"}

@app.post("/token")
def login():
    # For demo: static user
    return {"access_token": create_access_token({"sub": "developer"}), "token_type": "bearer"}

@app.post("/ask")
def ask_question(request: AskRequest, user=Depends(verify_token)):
    qa = get_qa_pipeline()
    response = qa.run(request.query)
    return {"answer": response}


@app.post("/convert")
def url_to_text(request: UrlConvertRequest):
    try:
        result = url_to_txt(request.url, "docs")
        return {"success": True, "message": f"URL converted successfully", "file_path": result}
    except Exception as e:
        return JSONResponse(content={"success": False, "error": str(e)}, status_code=500)

DOCS_DIR = "docs"  # same folder used in url_to_txt.py

@app.get("/list-docs")
def list_docs():
    """Return a list of all .txt files in the docs/data folder."""
    try:
        if not os.path.exists(DOCS_DIR):
            return {"docs": []}
        files = [
            f for f in os.listdir(DOCS_DIR)
            if f.endswith(".txt")
        ]
        return {"docs": sorted(files)}
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)