import streamlit as st
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from document_ingestion import ingest_document
from qa_service import answer_question
from web_search import search_artist_tour

st.set_page_config(page_title="🎤 Concert Tour Q&A", layout="centered")

st.title("🎤 Concert Tour RAG Assistant")
st.markdown("Upload concert tour documents and ask questions about them!")

tabs = st.tabs(["📄 Upload & Ingest", "💬 Ask a Question"])

# ------------------------------
# 📄 Tab 1: Document Ingestion
# ------------------------------
with tabs[0]:
    uploaded_file = st.file_uploader("Upload a .txt concert tour document", type="txt")
    if uploaded_file is not None:
        save_path = os.path.join("data/raw_docs", uploaded_file.name)
        with open(save_path, "wb") as f:
            f.write(uploaded_file.read())
        
        with st.spinner("Analyzing and summarizing document..."):
            result = ingest_document(save_path)

        if result.startswith("✅"):
            st.success("Ingestion completed!")
        else:
            st.warning("This document was not added.")
        st.markdown(f"**Result:**\n\n{result}")

# ------------------------------
# 💬 Tab 2: Question Answering
# ------------------------------
with tabs[1]:
    user_query = st.text_input("Ask a question about the concert tours:")
    if user_query:
        with st.spinner("Searching for an answer..."):
            response = answer_question(user_query)

            # Fallback to web if FAISS gives "Sorry" message
            if response.startswith("🤔"):
                st.info("Not found in local documents. Trying online search...")
                response = search_artist_tour(user_query)

        st.markdown("### 💬 Answer:")
        
        if "🌐 Retrieved via web search" in response:
            st.info("This answer was retrieved from publicly available web sources.")
            response = response.replace("🌐 Retrieved via web search", "")
        
        st.markdown(response)
