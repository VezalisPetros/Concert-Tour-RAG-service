from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from transformers import pipeline
import os
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


# Load the embedding model (same as ingestion)
embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Load the QA pipeline (using BART as a pseudo QA model)
qa_model = pipeline("summarization", model="facebook/bart-large-cnn")

# Load FAISS vector index from disk
faiss_index = FAISS.load_local(
    "data/processed/faiss_index",
    embeddings=embedding,
    allow_dangerous_deserialization=True
)


def answer_question(user_query: str) -> str:
    if not faiss_index:
        return "⚠️ The knowledge base is empty. Please upload and ingest documents first."

    # Step 1: Embed the query
    query_vector = embedding.embed_query(user_query)

    # Step 2: Get top 1 document to check similarity
    results = faiss_index.similarity_search(user_query, k=1)
    if not results:
        return "🤔 Sorry, I couldn't find any relevant info in the ingested documents."

    doc_vector = embedding.embed_query(results[0].page_content)
    similarity = cosine_similarity([query_vector], [doc_vector])[0][0]

    if similarity < 0.7:
        return "🤔 Sorry, I couldn't find anything related to your question."

    # Step 3: If relevant, do full RAG (get more chunks)
    results = faiss_index.similarity_search(user_query, k=3)
    context = "\n".join([doc.page_content for doc in results])

    if len(context.split()) > 1024:
        context = " ".join(context.split()[:1024])

    answer = qa_model(context + f"\n\nAnswer the question: {user_query}", max_length=130, min_length=30, do_sample=False)
    return answer[0]['summary_text']
