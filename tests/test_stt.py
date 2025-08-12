import pytest
from fastapi.testclient import TestClient
import os

from src.app import app
from src.stt.stt_transcriber import SttTranscriber

# Create test client
client = TestClient(app)

script_dir = os.path.dirname(os.path.abspath(__file__))

class TestSttAPI:

    def test_transcribe(self):
        assert(True)

class TestStt:

    def test_transcribe_english_mono(self):
        transcriber = SttTranscriber(language="en")
        result = transcriber.transcribe_file(os.path.join(script_dir, "audio/english_sample.wav"))
        assert(len(result) > 0)

    def test_transcribe_english_stereo(self):
        transcriber = SttTranscriber(language="en")
        result = transcriber.transcribe_file(os.path.join(script_dir, "audio/english_sample_stereo.wav"))
        assert(len(result) > 0)
    
    def test_transcribe_french_mp3(self):
        transcriber = SttTranscriber(language="fr")
        result = transcriber.transcribe_file(os.path.join(script_dir, "audio/french_sample.mp3"))
        assert(len(result) > 0)

