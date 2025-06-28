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
backend/    # FastAPI, LangGraph, Gemini, FAISS, ingestion, API
frontend/   # Minimal HTML/JS frontend
```

## Quickstart

### 1. Environment Variables
Create a `.env` file in `backend/` (or set via Docker):
```
GEMINI_API_KEY=your-gemini-api-key
```

### 2. Local Development
```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend
# (No build step needed; open frontend/index.html in your browser or serve statically)
```

### 3. Docker Compose
```bash
docker-compose up --build
```
- Backend: http://localhost:8000
- Frontend: http://localhost:8000 (served by FastAPI)

## API Endpoints (Summary)
- `POST /upload` — Upload document (PDF, TXT, etc.)
- `POST /add_wikipedia` — Add Wikipedia URL as knowledge
- `POST /chat` — Chat with the RAG bot (session-based)

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