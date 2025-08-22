from fastapi import FastAPI, UploadFile, HTTPException
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
from fastapi import Form

import os
import tempfile
import io

from .rag.rag import RAG
from .weather.llm import WeatherLLM
from .stt.stt_transcriber import SttTranscriber
from .tts.speech_generator import SpeechGenerator

api_prefix = os.getenv('API_PREFIX', "/services")

# Initialize FastAPI app with root_path prefix
app = FastAPI(root_path=api_prefix)




@app.get("/")
async def root():
    return {"message": "Minodu Service API"}

### RAG API ###

class RagRequest(BaseModel):
    conversation: str
    language: str
    question: str

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

### WEATHER LLM ###

class WeatherRequest(BaseModel):
    temperature: float
    humidity: float
    language: str


@app.post("/weather/text")
async def weather_text(request: WeatherRequest):
    weather_llm = WeatherLLM(language=request.language)

    def generate_stream():
        sensorData = WeatherLLM.SensorData(request.temperature, request.humidity)
        for chunk in weather_llm.ask_streaming(sensorData):
            yield chunk

    return StreamingResponse(
        generate_stream(),
        media_type="text/plain"
    )

### SPEECH TO TEXT API ###

class SttResponse(BaseModel):
    text: str

@app.post("/stt/transcribe", response_model=SttResponse)
async def stt_transcribe(file: UploadFile, language: str = Form(...)):
    transcriber = SttTranscriber(language=language)

    content = await file.read()
    
    data = io.BytesIO(content)
  
    result = transcriber.transcribe_file_buffer(data, file.filename)

    return SttResponse(
        text=result
    )



### TEXT TO SPEECH API ###

class TtsRequest(BaseModel):
    language: str
    text: str
    return_header: bool = True

@app.post("/tts/synthesize")
async def synthesize_speech(request: TtsRequest):
    try:
        generator = SpeechGenerator(request.language)
        
        def generate_audio():
            if request.return_header:
                header = SpeechGenerator.create_wav_header(generator.samplerate(), generator.channels())
                yield header

            for audio_chunk in generator.synthesize(request.text):
                yield audio_chunk
        
        return StreamingResponse(
            generate_audio(),
            media_type="audio/wav",
            headers={
                "Content-Disposition": "attachment; filename=speech.wav",
                "X-Sample-Rate": str(generator.samplerate()),
                "X-Channels": str(generator.channels())
            }
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Speech synthesis failed: {str(e)}")