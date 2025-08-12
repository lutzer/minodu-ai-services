from fastapi import FastAPI, UploadFile
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
from fastapi import Form

import os
import tempfile
import io

from .rag.rag import RAG
from .stt.stt_transcriber import SttTranscriber

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
    return {"message": "Minodu Service API"}

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
    text: str

@app.post("/stt/transcribe", response_model=SttResponse)
async def stt_transcribe(file: UploadFile, language: str = Form(...)):
    transcriber = SttTranscriber(language=language)

    content = await file.read()
    
    data = io.BytesIO(content)
  
    # Load MP3 file
    result = transcriber.transcribe_raw(data)
    
    # result = transcriber.transcribe_file(file.file)
    # return SttResponse(
    #     text=result
    # )
    return SttResponse(
        text=result
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