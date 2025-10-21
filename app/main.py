from fastapi import FastAPI, Depends
from app.auth import verify_token, create_access_token
from app.rag_pipeline import get_qa_pipeline
from app.url_to_txt import url_to_txt
import os
from fastapi.responses import JSONResponse

app = FastAPI(title="Generative AI Docs Q&A API")

@app.get("/")
def root():
    return {"message": "Welcome to Generative AI Q&A API"}

@app.post("/token")
def login():
    # For demo: static user
    return {"access_token": create_access_token({"sub": "developer"}), "token_type": "bearer"}

@app.post("/ask")
def ask_question(query: str, user=Depends(verify_token)):
    qa = get_qa_pipeline()
    response = qa.run(query)
    return {"answer": response}


@app.post("/convert")
def url_to_text(url: str, output_filename: str):
    url_to_txt(url, output_filename)

DOCS_DIR = "data"  # same folder used in url_to_txt.py

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