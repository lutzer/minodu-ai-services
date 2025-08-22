import pytest
from fastapi.testclient import TestClient
import os

from src.app import app

# Create test client
client = TestClient(app)

class TestWeatherAPI:

    def test_weather_text(self):
        test_data = {
            "temperature": 25.0,
            "humidity": 0.5,
            "language": "en"
        }
        response = client.post(app.root_path + "/weather/text", json=test_data)        
        assert response.status_code == 200
        assert len(response.text) > 0