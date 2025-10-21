from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_community.chat_models import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DOCS_PATH = os.getenv("DOCS_PATH")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")

print(f"Debug {DOCS_PATH}")

def build_vectorstore():
    loader = DirectoryLoader(DOCS_PATH, glob="**/*.txt", loader_cls=TextLoader)
    docs = loader.load()
    # helps split them into 1000 character blocks 
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    texts = splitter.split_documents(docs)

    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)
    db = FAISS.from_documents(texts, embeddings)
    db.save_local("faiss_index")

def get_qa_pipeline():
    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)
    db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)

    retriever = db.as_retriever(search_kwargs={"k": 4})
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
    return qa_chain

# Optional: Pre-build the index when first running
if not os.path.exists("faiss_index"):
    build_vectorstore()
