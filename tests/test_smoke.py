import pytest
from fastapi.testclient import TestClient
import sys
import os

# Adjust path to include backend directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend')))

from main import app

@pytest.fixture
def client():
    return TestClient(app)

def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to BharatAI Citizen Assistant API"}
