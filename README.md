# 🎵 Concert Tour Q&A Assistant (RAG + Web Search)

This project is a domain-specific document ingestion and question-answering assistant designed for upcoming **concert tours (2025–2026)**. It uses **RAG (Retrieval-Augmented Generation)** to answer questions strictly based on ingested concert documents and optionally uses **web search** to answer artist-related queries not found in local data.

---

## 🔄 Core Functionality

### 1. 📄 Document Ingestion
- Upload `.txt` files containing concert-related info (e.g. tour plans, dates, venues).
- System determines if the document is related to **concerts/touring** using keyword checks.
- If relevant:
  - A summarizer (BART-based) generates a concise summary.
  - The summary is embedded using MiniLM and stored in **FAISS**.
- If not:
  - User gets a polite message saying it's not a concert-related document.

### 2. 🤔 Question Answering (RAG-based)
- User types a natural-language question (e.g. _"Where is Lady Gaga performing in autumn 2025?"_)
- System searches FAISS for relevant summaries using vector similarity.
- If similarity is high enough, context is passed to the summarization model to answer.
- If no relevant data is found, a fallback message is shown.

### 3. 🌐 (Bonus) Web Search Mode
If the system cannot answer based on local data:
- Extracts the likely artist name from the query (e.g. _"Beyoncé"_ from _"Is Beyoncé touring in 2026?"_)
- Uses **SerpAPI** to search Google for real-time concert info.
- Parses top results and returns snippets about concerts/tours.
- Web results are clearly marked with: “*Retrieved from web*”

---

## 🎨 Tech Stack

| Component       | Tech Used |
|----------------|-----------|
| Language Models| Hugging Face Transformers (BART summarizer) |
| Embeddings     | MiniLM via `sentence-transformers` |
| Vector Store   | FAISS     |
| UI             | Streamlit |
| Web Search     | SerpAPI (`google-search-results`) |
| Storage        | SQLite + `sqlite-utils` |
| Config         | `.env` with `python-dotenv` |

---

## 🚫 Known Limitations

### Keyword-Based Relevance Filter (Ingestion)
The system uses a keyword filter to detect whether a document is concert-related. This works well for most cases but may produce:
- ✅ **False Positives** (e.g., business reports with words like "performance" or "schedule")
- ❌ **False Negatives** (e.g., less obvious concert docs)

> ✨ Future enhancement: use a text classifier or zero-shot classification for more accurate filtering.

---

## ⚡ Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/ProvectusInternship_YourNameCamelCase.git
cd ProvectusInternship_YourNameCamelCase
```
### 2.  Create & Activate Virtual Environment
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
```
### 3.  Install Dependencies
```bash
pip install -r requirements.txt
```
### 4. Add Environment Variables
```bash
SERPAPI_KEY=your_serpapi_key_here
```
### 5. Run the App
```bash
streamlit run ui/app.py
