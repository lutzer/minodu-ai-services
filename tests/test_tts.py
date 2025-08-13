import pytest
from fastapi.testclient import TestClient
import os
import json

from src.app import app
from src.tts.speech_generator import SpeechGenerator

# Create test client
client = TestClient(app)

script_dir = os.path.dirname(os.path.abspath(__file__))

class TestTtsAPI:

    def test_synthesize(self):
        test_data = {
            "text": "Hello Api, synthesize this",
            "language": "en"
        }
        response = client.post(app.root_path + "/tts/synthesize", json=test_data)        
        assert response.status_code == 200
        assert(len(response.content) > 0)

class TestTts:

    def test_synthesize_some_data_en(self):
        generator = SpeechGenerator("en")

        audio_chunks = []
        
        for audio_chunk in generator.synthesize("Hello, how are you? This is an Example Text."):
            audio_chunks.append(audio_chunk)

        assert(len(audio_chunks) > 0)

    def test_synthesize_some_data_fr(self):
        generator = SpeechGenerator("fr")

        audio_chunks = []
        
        for audio_chunk in generator.synthesize("Bonjour. Comment allez vous?"):
            audio_chunks.append(audio_chunk)

        assert(len(audio_chunks) > 0)
    
    def test_create_wav(self):
        output_path = os.path.join(script_dir, "output.wav")

        generator = SpeechGenerator("en")

        audio_chunks = []
        
        for audio_chunk in generator.synthesize("Hello, how are you? This is an Example Text."):
            audio_chunks.append(audio_chunk)

        buffer = SpeechGenerator.generate_wav(audio_chunks, generator.channels(), generator.samplerate())

        buffer.seek(0)  # Reset position to beginning
        with open(output_path, "wb") as f:
            f.write(buffer.read())

        assert(os.path.exists(output_path))

        os.remove(output_path)


   

