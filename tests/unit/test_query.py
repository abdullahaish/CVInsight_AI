from fastapi.testclient import TestClient
from unittest.mock import patch
import os
import sys

# Add project root to PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from main import app
import pytest
from mongomock import MongoClient

client = TestClient(app)

@pytest.fixture
def mock_mongo_client():
    """Creates a mock MongoDB client."""
    return MongoClient()

@patch("app.config.client")
def test_chatbot_query(mock_mongo, mock_mongo_client):
    """Test chatbot query with mocked MongoDB."""
    mock_mongo.return_value = mock_mongo_client
    with patch("app.services.llm_analysis.analyze_query", return_value={"skills": {"$regex": "Python", "$options": "i"}}):
        response = client.get("/chatbot/?query=Find candidates with Python skills")
    assert response.status_code == 200
    assert "query" in response.json()
    assert response.json()["query"] == "Find candidates with Python skills"
    assert "results" in response.json()

@patch("app.config.client")
def test_chatbot_query_no_results(mock_mongo, mock_mongo_client):
    """Test chatbot query with a skill that doesn't exist in database."""
    mock_mongo.return_value = mock_mongo_client
    with patch("app.services.llm_analysis.analyze_query", return_value={"skills": {"$regex": "COBOL", "$options": "i"}}):
        response = client.get("/chatbot/?query=Find candidates with COBOL skills")
    assert response.status_code == 200
    assert "query" in response.json()
    assert response.json()["query"] == "Find candidates with COBOL skills"
    assert "results" in response.json()
    assert response.json()["results"] == []