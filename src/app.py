from fastapi import FastAPI, UploadFile
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


class SttResponse(BaseModel):
    language: str
    text: str

@app.post("/stt/transcribe", response_model=SttResponse)
async def stt_transcribe(file: UploadFile):
    return SttResponse(
        text=file.size
    )

class TtsRequest(BaseModel):
    language: str
    text: str

@app.post("/tts/speak")
async def stt_transcribe(request: TtsRequest):

    def generate_stream():
        for chunk in rag.ask_streaming(request.question, request.conversation):
            yield chunk

    return StreamingResponse(
        generate_stream(), 
        media_type="audio/mp3"
    )