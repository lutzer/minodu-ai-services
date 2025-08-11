import pytest
from fastapi.testclient import TestClient
import os

from src.app import app

# Create test client
client = TestClient(app)

class TestAPI:

    def test_rag_ask(self):
        test_data = {
            "question": "Hello how are you?",
            "conversation" : "",
            "language": "en"
        }
        response = client.post(app.root_path + "/rag/ask", json=test_data)
        
        assert response.status_code == 200
        response_data = response.json()
        
        assert len(response_data["answer"]) > 0
        
if __name__ == "__main__":
    # Run tests if script is executed directly
    pytest.main([__file__, "-v"])