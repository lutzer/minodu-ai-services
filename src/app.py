from fastapi import FastAPI
from pydantic import BaseModel
import os

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

@app.post("/rag/ask", response_model=RagResponse)
async def rag_ask(request: RagRequest):
    print("rag ask")
    rag = RAG(request.language)
    result = rag.ask(request.question, request.conversation, stream=False)

    response = RagResponse(
        status="success",
        answer=result
    )
    return response