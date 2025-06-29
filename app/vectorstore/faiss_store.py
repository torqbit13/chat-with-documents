from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from loguru import logger
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from app.config import (
    CHUNK_OVERLAP,
    CHUNK_SIZE,
    EMBEDDING_MODEL_NAME,
    GOOGLE_API_KEY,
)


class SessionVectorStore:
    _stores = {}  # session_id -> vectorstore
    _embeddings = GoogleGenerativeAIEmbeddings(
        model=EMBEDDING_MODEL_NAME, google_api_key=GOOGLE_API_KEY
    )
    _splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP
    )

    @classmethod
    def add_documents(cls, session_id, docs):
        store = cls._stores.get(session_id)
        if store is None:
            logger.info(f"Creating new vector store for session {session_id}")
            store = FAISS.from_documents(docs, cls._embeddings)
        else:
            logger.info(f"Using the same vector store for session {session_id}")
            store.add_documents(docs)
        cls._stores[session_id] = store

    @classmethod
    def chunk_text(cls, text):
        return cls._splitter.create_documents([text])

    @classmethod
    def get_retriever(cls, session_id):
        store = cls._stores.get(session_id)
        if store is None:
            return None
        return store.as_retriever()
