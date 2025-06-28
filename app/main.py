from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
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

# Serve static files (if you add JS/CSS later, put them in frontend/ and reference as /static/filename)
app.mount(
    "/static",
    StaticFiles(
        directory=os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../frontend")
        )
    ),
    name="static",
)


# Serve index.html at root
@app.get("/")
def root():
    return FileResponse(
        os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../frontend/index.html")
        )
    )
