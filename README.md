---
title: RAG Document Q&A
emoji: 📄
colorFrom: blue
colorTo: indigo
sdk: docker
pinned: false
license: mit
---

# RAG Document Q&A System

A document question-answering system built with FastAPI, ChromaDB, Sentence Transformers, and Groq's Llama-3.3-70B. Upload any PDF and ask questions in natural language — answers come back with page-level citations.

## Stack

| Layer | Tech |
|---|---|
| Backend API | FastAPI |
| Vector Store | ChromaDB |
| Embeddings | Sentence Transformers (all-MiniLM-L6-v2) |
| LLM | Groq — Llama-3.3-70B |
| Frontend | Streamlit |
| Analytics | SQLite |
| Containerization | Docker |

## Features

- Upload any PDF via the Streamlit UI
- Automatic text extraction, cleaning, and chunking
- Cosine similarity retrieval with configurable top-k and threshold
- Page-level source citations on every answer
- Analytics dashboard: response latency, frequent queries, unanswered queries
- Collection reset on new upload — no bleed between documents

## Usage

1. Upload a PDF using the sidebar file uploader
2. Click **Ingest Document** and wait for chunking to complete
3. Ask questions in the chat input
4. Answers include page citations and similarity scores
5. Switch to **Analytics** in the sidebar to view query stats

## Run Locally

```bash
git clone https://github.com/dhruv-motaval/rag-document-qa
cd rag-document-qa
cp .env.example .env
# Add your GROQ_API_KEY to .env

# Terminal 1
uvicorn app.main:app --reload

# Terminal 2
streamlit run streamlit_app.py
```

Get a free Groq API key at [console.groq.com](https://console.groq.com)

## Configuration

| Variable | Default | Description |
|---|---|---|
| `CHUNK_SIZE` | 1000 | Characters per chunk |
| `CHUNK_OVERLAP` | 200 | Overlap between chunks |
| `TOP_K` | 4 | Chunks retrieved per query |
| `SIMILARITY_THRESHOLD` | 0.7 | Max cosine distance before "not found" |

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/ingest` | Upload and ingest a PDF |
| `POST` | `/ask` | Ask a question |
| `GET` | `/analytics` | Get usage analytics |
| `GET` | `/health` | Health check |
