from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import os

def get_vector_store(documents, persist_path="vector_store"):
    # 1. Use consistent embedding model
    MODEL_NAME = "google/flan-t5-base"
    embeddings = HuggingFaceEmbeddings(model_name=MODEL_NAME)
    
    # 2. Verify embedding dimensions
    sample_embedding = embeddings.embed_query("Test")
    embedding_dim = len(sample_embedding)
    print(f"[Embedding Log] Using model '{MODEL_NAME}' with dimension {embedding_dim}")

    # 3. Add dimension verification when loading existing index
    if os.path.exists(persist_path):
        try:
            # Check if existing index matches current embedding dimension
            index = FAISS.load_local(persist_path, embeddings, allow_dangerous_deserialization=True)
            print("[Vector Store] Loaded existing index with matching dimensions")
            return index
        except Exception as e:
            print(f"[Vector Store] Error loading existing index: {str(e)}")
            print("[Vector Store] Rebuilding index...")
            # Remove corrupted/incompatible index
            shutil.rmtree(persist_path)

    # 4. Create new index with verified dimensions
    print("[Vector Store] Creating new index")
    vector_store = FAISS.from_documents(documents, embeddings)
    
    # 5. Verify before saving
    assert vector_store.index.ntotal == len(documents), "Document count mismatch"
    vector_store.save_local(persist_path)
    
    return vector_store
