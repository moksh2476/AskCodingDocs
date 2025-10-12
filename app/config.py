import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DOCS_PATH = "./docs"
EMBEDDING_MODEL = "text-embedding-3-small"
