import pytest
from fastapi.testclient import TestClient
import os
import json

from src.app import app
from src.stt.stt_transcriber import SttTranscriber

# Create test client
client = TestClient(app)

script_dir = os.path.dirname(os.path.abspath(__file__))

class TestSttAPI:

    def test_transcribe_mono(self):
        file_path = os.path.join(script_dir, "audio/english_sample_mono.wav")
        with open(file_path, "rb") as f:
            response = client.post(
                "/stt/transcribe",
                files={"file": (os.path.basename(file_path), f, "audio/wav")},
                data={"language": "en"}
            )
    
        assert response.status_code == 200
        data = response.json()
        assert(len(data["text"]) > 0)
    
    def test_transcribe_stereo(self):
        file_path = os.path.join(script_dir, "audio/english_sample_stereo.wav")
        with open(file_path, "rb") as f:
            response = client.post(
                "/stt/transcribe",
                files={"file": (os.path.basename(file_path), f, "audio/wav")},
                data={"language": "en"}
            )
    
        assert response.status_code == 200
        data = response.json()
        assert(len(data["text"]) > 0)

    def test_transcribe_mp3(self):
        file_path = os.path.join(script_dir, "audio/french_sample.mp3")
        with open(file_path, "rb") as f:
            response = client.post(
                "/stt/transcribe",
                files={"file": (os.path.basename(file_path), f, "audio/wav")},
                data={"language": "fr"}
            )
    
        assert response.status_code == 200
        data = response.json()
        assert(len(data["text"]) > 0)

class TestStt:

    def test_transcribe_english_mono(self):
        transcriber = SttTranscriber(language="en")
        with open(os.path.join(script_dir, "audio/english_sample_mono.wav"), "rb") as file:
            result = transcriber.transcribe_file(file)
        assert(len(result) > 0)

    def test_transcribe_english_stereo(self):
        transcriber = SttTranscriber(language="en")
        with open(os.path.join(script_dir, "audio/english_sample_stereo.wav"), "rb") as file:
            result = transcriber.transcribe_file(file)
        assert(len(result) > 0)
    
    def test_transcribe_french_mp3(self):
        transcriber = SttTranscriber(language="fr")
        with open(os.path.join(script_dir, "audio/french_sample.mp3"), "rb") as file:
            result = transcriber.transcribe_file(file)
        assert(len(result) > 0)

