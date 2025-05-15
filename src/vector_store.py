from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import os

def get_vector_store(documents, persist_path="vector_store"):
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

    if os.path.exists(persist_path):
        return FAISS.load_local(persist_path, embeddings)
    
    vector_store = FAISS.from_documents(documents, embeddings)
    vector_store.save_local(persist_path)
    return vector_store
