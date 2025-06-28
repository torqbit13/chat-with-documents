from loguru import logger
from fastapi import APIRouter, UploadFile, File, HTTPException, Body
from pydantic import BaseModel
from backend.app.vectorstore.faiss_store import VectorStoreSingleton
from backend.app.utils.file_parser import parse_file
from backend.app.utils.wikipedia import fetch_wikipedia_content
from backend.app.chat.langgraph_manager import langgraph_manager

router = APIRouter()

class WikiRequest(BaseModel):
    url: str

@router.post("/upload")
def upload_file(file: UploadFile = File(...)):
    try:
        #Document Ingestion
        text = parse_file(file)
        #Text Chunking
        docs = VectorStoreSingleton.chunk_text(text)
        logger.debug(f"Splited docs: {docs}")
        #Embedding Generation & Vector Storage
        VectorStoreSingleton.add_documents(docs)
        return {"message": "File uploaded, chunked, and indexed successfully."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/add_wikipedia")
def add_wikipedia(request: WikiRequest):
    try:
        #Document Ingestion
        url = request.url
        title, text = fetch_wikipedia_content(url)
        logger.info(f"Title of the wikipedia Article: {title}")
        #Text Chunking
        docs = VectorStoreSingleton.chunk_text(f"{title}\n{text}")
        logger.debug(f"Wikipedia article chunks: {docs}")
        #Embedding Generation & Vector Storage
        VectorStoreSingleton.add_documents(docs)
        return {"message": f"Wikipedia article '{title}' chunked and indexed."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/start_session")
def start_session():
    session_id = langgraph_manager.start_session()
    return {"session_id": session_id}


@router.post("/chat")
def chat(session_id: str = Body(...), query: str = Body(...)):
    result = langgraph_manager.chat(session_id, query)
    return result
