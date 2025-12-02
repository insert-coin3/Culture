from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from public_data import fetch_public_data

def build_vector_store():
    texts = fetch_public_data()
    if not texts:
        print("No texts found. Vector store cannot be built.")
        return None

    try:
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        vector_store = FAISS.from_texts(texts, embeddings)
        return vector_store
    except Exception as e:
        print(f"Error building vector store: {e}")
        return None
