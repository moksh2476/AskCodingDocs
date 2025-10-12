from fastapi import FastAPI, Depends
from app.auth import verify_token, create_access_token
from app.rag_pipeline import get_qa_pipeline

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
