import pytest
from fastapi.testclient import TestClient
from ..main import app

# Create test client
client = TestClient(app)

class TestAPI:
    """Unit tests for the FastAPI application"""

    def test_send_message_success(self):
        """Test successful message sending"""
        test_data = {
            "message": "Hello, World!",
            "user_id": "test_user_123"
        }
        
        response = client.post("/send-message", json=test_data)
        
        assert response.status_code == 200
        response_data = response.json()
        
        assert response_data["status"] == "success"
        assert response_data["received_message"] == test_data["message"]
        assert response_data["user_id"] == test_data["user_id"]



if __name__ == "__main__":
    # Run tests if script is executed directly
    pytest.main([__file__, "-v"])