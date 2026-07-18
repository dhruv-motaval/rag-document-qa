# RAG Document Q&A System

A Retrieval-Augmented Generation (RAG) system that answers questions about any PDF document using semantic search and LLM-powered question answering. Full LangSmith tracing on every query for latency, token, and cost observability.

Built with **FastAPI**, **LangChain**, **ChromaDB**, **Sentence Transformers**, **Groq**, **LangSmith**, **SQLite**, and **Streamlit**.

**Live demo:** [huggingface.co/spaces/MotavalD/Rag-Document-Qa](https://huggingface.co/spaces/MotavalD/Rag-Document-Qa)

---

## Architecture

```text
PDF Document
    │
    ▼
PyMuPDF (Text Extraction)
    │
    ▼
Text Cleaning + Chunking
    │
    ▼
Sentence Transformers
(all-MiniLM-L6-v2)
    │
    ▼
Embeddings
    │
    ▼
ChromaDB (Vector Store)
    │
    ▼
User Query
    │
    ▼
Query Embedding
    │
    ▼
Similarity Search (Top-K)
    │
    ▼
Retrieved Chunks
    │
    ▼
LangChain → Groq Llama-3.3-70B
    │              │
    ▼              ▼
Answer + Sources   LangSmith Trace
    │
    ▼
FastAPI
```

## Stack

| Layer | Tech |
|---|---|
| Backend API | FastAPI |
| Vector Store | ChromaDB |
| Embeddings | Sentence Transformers (all-MiniLM-L6-v2) |
| LLM | Groq — Llama-3.3-70B |
| Orchestration | LangChain |
| Observability | LangSmith |
| Frontend | Streamlit |
| Analytics | SQLite |
| Containerization | Docker |

## Features

- Upload any PDF via the Streamlit UI
- Automatic text extraction, cleaning, and chunking
- Cosine similarity retrieval with configurable top-k and threshold
- Page-level source citations on every answer
- Strict grounding — the model responds with "Information not found in document" rather than hallucinating when retrieved context doesn't support an answer
- Full LangSmith tracing: latency, token usage, cost, and input/output logged per chain invocation
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
# Add your GROQ_API_KEY, LANGCHAIN_API_KEY to .env
```

Using `uv`:

```bash
uv sync

# Terminal 1
uv run uvicorn app.main:app --reload

# Terminal 2
uv run streamlit run streamlit_app.py
```

Or with `pip`:

```bash
pip install -r requirements.txt

# Terminal 1
uvicorn app.main:app --reload

# Terminal 2
streamlit run streamlit_app.py
```

Get a free Groq API key at [console.groq.com](https://console.groq.com)
Get a free LangSmith API key at [smith.langchain.com](https://smith.langchain.com)

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `GROQ_API_KEY` | Yes | Groq API key for LLM calls |
| `LANGCHAIN_API_KEY` | Optional | Enables LangSmith tracing |
| `LANGCHAIN_TRACING_V2` | Optional | Set to `true` to enable tracing |
| `LANGCHAIN_PROJECT` | Optional | LangSmith project name, defaults to `default` |

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

## Roadmap

- [ ] Agentic RAG flow with LangGraph (query rewrite → retrieve → grade → decide)
- [ ] Migrate to Qdrant with BM25 hybrid search + RRF fusion
- [ ] RAGAS evaluation suite with before/after metrics
