import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_admin():
    admin_data = {
        "username": "testuser",
        "email": "test@example.com"
    }
    
    response = client.post("/admin/", json=admin_data)
    
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert "id" in data

def test_get_admins():
    response = client.get("/admin/")
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)