from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
import os

def print_faiss_contents():
    index_path = "data/processed/faiss_index"
    embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    if not os.path.exists(index_path):
        print("No FAISS index found.")
        return

    db = FAISS.load_local(index_path, embedding, allow_dangerous_deserialization=True)
    docs = db.similarity_search("show everything", k=10)

    print("🔍 Documents in FAISS:")
    for i, doc in enumerate(docs, 1):
        print(f"\n--- Document {i} ---")
        print(doc.page_content)
        print("Metadata:", doc.metadata)
