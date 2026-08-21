from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from pypdf import PdfReader
# Resume analyzer using RAG and LLM

# RAG Document loading/extract
def extract_pdf(file):
    reader = PdfReader(file)
    text = "" #str type
    for page in reader.pages:
        text += page.extract_text()
    return text

# Splliting
def split_text(text):
    splitter = RecursiveCharacterTextSplitter(chunk_size=250, chunk_overlap=50) 
    return splitter.split_text(text)

# Embeddings and vector store
def create_vector_store(text):
    chunks = split_text(text)
    docs = [Document(page_content=c) for c in chunks]
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(docs, embeddings)
    return vectorstore

# 