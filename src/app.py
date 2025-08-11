from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
import os
import json

from .rag.rag import RAG

api_prefix = os.getenv('API_PREFIX', "/services")

# Initialize FastAPI app with root_path prefix
app = FastAPI(root_path=api_prefix)

# Request model
class RagRequest(BaseModel):
    conversation: str
    language: str
    question: str

# Response model
class RagResponse(BaseModel):
    status: str
    answer: str

@app.get("/")
async def root():
    return {"message": "Simple FastAPI boilerplate"}

@app.post("/rag/ask")
async def rag_ask(request: RagRequest):
    rag = RAG(language=request.language)

    def generate_stream():
        for chunk in rag.ask_streaming(request.question, request.conversation):
            yield chunk

    return StreamingResponse(
        generate_stream(),
        media_type="text/plain"
    )