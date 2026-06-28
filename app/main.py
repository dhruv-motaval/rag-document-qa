from app.schemas import AskResponse, AnalysticsResponse, AskRequest
from fastapi import FastAPI, HTTPException, UploadFile, File, status
from fastapi.responses import JSONResponse
import time
import os
import shutil
import traceback

from app.ingest import ingest_document, chroma_client
from app.rag import answer_question
from app.analytics import get_analytics
from app.db import init_db, log_query

app = FastAPI()


@app.on_event("startup")
def startup():
    init_db()


@app.get("/")
def root():
    return {"message": "RAG API RUNNING"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/ingest")
async def ingest(file: UploadFile = File(...)):
    # Reset collection so previous document doesn't bleed into new one
    try:
        chroma_client.delete_collection("document_collection")
        chroma_client.get_or_create_collection(
            name="document_collection", metadata={"hnsw:space": "cosine"}
        )
    except Exception:
        pass

    temp_path = f"temp_{file.filename}"

    try:
        with open(temp_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        result = ingest_document(temp_path)
        return result

    except Exception as e:
        traceback.print_exc()  # prints full traceback to terminal
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)


@app.post("/ask", response_model=AskResponse)
def ask(request: AskRequest):
    question = request.question.strip()

    if not question:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid question"
        )

    start_time = time.time()
    result = answer_question(question)
    latency_ms = (time.time() - start_time) * 1000

    log_query(
        question=question, answer_found=result["answer_found"], latency_ms=latency_ms
    )

    return result


@app.get("/analytics", response_model=AnalysticsResponse)
def analytics():
    return get_analytics()