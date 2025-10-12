from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from app.config import OPENAI_API_KEY, DOCS_PATH, EMBEDDING_MODEL
import os

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

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
