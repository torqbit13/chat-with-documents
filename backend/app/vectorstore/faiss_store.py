from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from loguru import logger
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from backend.app.config import (
    CHUNK_OVERLAP,
    CHUNK_SIZE,
    EMBEDDING_MODEL_NAME,
    GOOGLE_API_KEY,
)

class VectorStoreSingleton:
    _vectorstore = None
    _retriever = None
    _embeddings = GoogleGenerativeAIEmbeddings(
        model=EMBEDDING_MODEL_NAME, google_api_key=GOOGLE_API_KEY
    )
    _splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)

    @classmethod
    def add_documents(cls, docs):
        if cls._vectorstore is None:
            logger.info("inside the if block of creating the retriever:")
            cls._vectorstore = FAISS.from_documents(docs, cls._embeddings)
        else:
            cls._vectorstore.add_documents(docs)
        cls._retriever = cls._vectorstore.as_retriever()

    @classmethod
    def chunk_text(cls, text):
        return cls._splitter.create_documents([text])

    @classmethod
    def get_retriever(cls):
        return cls._retriever


