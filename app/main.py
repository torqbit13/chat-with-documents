from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from .api.routes import router as api_router

app = FastAPI(title="RAG Chatbot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

# Serve static files 
app.mount(
    "/",
    StaticFiles(
        directory=os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../frontend")
        ),
        html=True,
    ),
    name="static",
)
