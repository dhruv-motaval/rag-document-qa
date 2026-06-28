FROM python:3.11-slim

WORKDIR /app

# Install system dependencies needed by PyMuPDF and ChromaDB
RUN apt-get update && apt-get install -y \
    build-essential \
    libglib2.0-0 \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies first (layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ ./app/
COPY streamlit_app.py .

# Create directories for runtime storage
RUN mkdir -p chroma_db

# HuggingFace Spaces only exposes 7860
EXPOSE 7860

# Start FastAPI on 8000 in background, Streamlit on 7860 in foreground
CMD uvicorn app.main:app --host 0.0.0.0 --port 8000 & \
    sleep 3 && \
    streamlit run streamlit_app.py \
    --server.port 7860 \
    --server.address 0.0.0.0 \
    --server.fileWatcherType none
