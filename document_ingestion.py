import os
from dotenv import load_dotenv
import sqlite3

from langchain_huggingface import HuggingFaceEmbeddings

from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import TextLoader
from langchain.schema import Document
from transformers import pipeline


def is_concert_related(text: str) -> bool:
    concert_keywords = [
        "concert", "tour", "musician", "band", "singer", "performer",
        "live show", "special guest", "venue", "stage design",
        "tour bus", "soundcheck", "backstage", "lighting rig"
    ]

    text_lower = text.lower()
    return any(kw in text_lower for kw in concert_keywords)


# Load summarization pipeline once
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

from transformers import pipeline

# Global summarizer pipeline
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_text(text: str) -> str:
    prompt = (
        "Please summarize the following concert tour document clearly. "
        "Include specific cities, dates, venues, guest performers, and logistics info:\n\n"
        + text
    )

    max_input = 1024
    if len(prompt.split()) > max_input:
        prompt = " ".join(prompt.split()[:max_input])

    summary = summarizer(prompt, max_length=130, min_length=30, do_sample=False)
    return summary[0]['summary_text']



def save_summary_to_db(doc_id: str, summary: str):
    conn = sqlite3.connect("data/summary_store.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS summaries (
            id TEXT PRIMARY KEY,
            summary TEXT
        )
    """)
    cursor.execute("INSERT OR REPLACE INTO summaries (id, summary) VALUES (?, ?)", (doc_id, summary))
    conn.commit()
    conn.close()

import os

def save_summary_to_vectorstore(doc_id: str, summary: str):
    embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = text_splitter.create_documents([summary])

    for doc in chunks:
        doc.metadata = {"id": doc_id}

    index_path = "data/processed/faiss_index"

    if os.path.exists(index_path):
        db = FAISS.load_local(index_path, embedding, allow_dangerous_deserialization=True)
        db.add_documents(chunks)
    else:
        db = FAISS.from_documents(chunks, embedding)

    db.save_local(index_path)


def ingest_document(doc_path: str) -> str:
    loader = TextLoader(doc_path)
    docs = loader.load()
    full_text = docs[0].page_content

    # 🔒 Make sure to reject irrelevant docs
    if not is_concert_related(full_text):
        return "❌ Sorry, I cannot ingest documents with other themes."

    # ✅ Process concert-related docs
    summary = summarize_text(full_text)
    doc_id = os.path.basename(doc_path)

    save_summary_to_db(doc_id, summary)
    save_summary_to_vectorstore(doc_id, summary)

    return f"✅ Document ingested successfully! Here's a summary:\n\n{summary}"

