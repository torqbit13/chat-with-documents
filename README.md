# Modular RAG Chatbot System (LangGraph + FastAPI + Gemini)

## Overview
A production-grade, modular Retrieval-Augmented Generation (RAG) chatbot system using LangGraph, FastAPI, Gemini LLM, FAISS, and a minimal HTML/JS frontend. Accepts user-uploaded documents and Wikipedia URLs as knowledge sources. Exposes RESTful API and a minimal web frontend. Session-based conversational memory and LangSmith tracing are supported.

## Features
- Upload documents or add Wikipedia URLs as knowledge
- Gemini embeddings + FAISS vector store
- LangGraph for conversational flow and memory
- RESTful endpoints via FastAPI
- Minimal HTML/JS frontend
- Fully containerized (Docker)
- LangSmith tracing support for observability

## Folder Structure
```
app/         # Backend (FastAPI, LangGraph, Gemini, FAISS, ingestion, API)
frontend/    # Minimal HTML/JS frontend (index.html, etc.)
requirements.txt
Dockerfile
README.md
```

## Quickstart

### 1. Environment Variables
Create a `.env` file in the project root (or set via Docker):
```
GEMINI_API_KEY=your-gemini-api-key
```

### 2. Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run the backend (serves both API and frontend)
uvicorn app.main:app --reload

# Visit the app in your browser:
# http://localhost:8000/
```

### 3. Docker Build & Run
```bash
docker build -t rag-chatbot .
docker run -p 8000:8000 --env-file .env rag-chatbot
```
- The backend and frontend will both be available at: http://localhost:8000/

## API Endpoints (Summary)
- `POST /upload` — Upload document (PDF, TXT, etc.)
- `POST /add_wikipedia` — Add Wikipedia URL as knowledge
- `POST /chat` — Chat with the RAG bot (session-based)
- `POST /start_session` — Start a new chat session

## Tech Stack
- FastAPI, LangGraph, LangChain, Gemini LLM, FAISS, Docker, HTML/JS

## LangSmith Tracing (Optional)
To enable tracing, set these environment variables:
```
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your-langsmith-key
LANGCHAIN_PROJECT=your-project-name
```

## License
MIT 