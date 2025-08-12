import pytest
from fastapi.testclient import TestClient
import os

from src.app import app

# Create test client
client = TestClient(app)

class TestAPI:

    @pytest.mark.skip()
    def test_rag_ask(self):
        test_data = {
            "question": "This is a generic question.",
            "conversation" : "",
            "language": "en"
        }
        response = client.post(app.root_path + "/rag/ask", json=test_data)
        
        assert response.status_code == 200

        print(response.text)
        
        assert len(response.text) > 0