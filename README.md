# 🎵 Concert Tour Q&A Assistant (RAG + Web Search)

This project is a domain-specific document ingestion and question-answering assistant designed for upcoming **concert tours (2025–2026)**. It uses **RAG (Retrieval-Augmented Generation)** to answer questions strictly based on ingested concert documents and optionally uses **web search** to answer artist-related queries not found in local data.

---


## 🔄 Core Functionality & Design Choices

### 1. 📄 Document Ingestion

- Users upload plain `.txt` documents related to tours, concerts, schedules, and logistics.
- Documents are filtered using a keyword-based concert detector to reject unrelated files (e.g. business reports).  
  > 🛠 **Design Choice**: We used a keyword matcher for simplicity; while not perfect, it performs well for MVP. Future work could use a lightweight classifier.

- For relevant docs:
  - A summary is generated using the **`facebook/bart-large-cnn`** model from Hugging Face.
    > 🧠 **Why BART from Hugging Face?** It’s free, open-source, doesn’t require OpenAI API keys, and gives strong summarization for factual text.

  - The summary is embedded using **MiniLM** (via `sentence-transformers`) and stored in a FAISS index.
    > 💾 **Why FAISS?** Fast local vector search, better for semantic similarity than using SQLite alone.

---

### 2. 🤔 Question Answering (RAG-based)

- The user can ask natural language questions (e.g., *"Where is Lady Gaga performing?"*).
- The system:
  1. Embeds the question
  2. Finds the most similar document summaries using FAISS
  3. If similarity is high enough, constructs an answer using the summarization model
  4. If nothing relevant is found, gracefully declines to answer

> 🔒 We added a **similarity threshold** so irrelevant results (like “Gaga” answers for a “Beyoncé” question) are not returned.

---

### 3. 🌐 Web Search Mode

If no local data answers the question:
- The assistant falls back to a web search using **SerpAPI** (Google Search wrapper)
- Extracts the artist name from the query using heuristics
- Queries public results like: `"Taylor Swift 2025 2026 tour schedule"`
- Returns a few clean snippets
- UI clearly shows the info was retrieved via web

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




## 🛠️ Project Structure

```plaintext
provectus_concert_bot/
├── data/
│   ├── raw_docs/           # Uploaded raw text files
│   └── processed/          # FAISS index
├── ui/
│   └── app.py              # Streamlit interface
├── document_ingestion.py   # Ingest/summarize/filter docs
├── qa_service.py           # RAG question-answering logic
├── web_search.py           # Artist lookup via web
├── utils.py                # Helper/debug tools
├── setup.sh                # One-click setup script
├── requirements.txt
├── .env
└── README.md
```
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
```


