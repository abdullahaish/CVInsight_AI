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
def sample_pdf():
    """Creates a temporary sample PDF file for testing."""
    file_path = "test_sample.pdf"
    with open(file_path, "wb") as f:
        f.write(b"This is a test PDF content.")
    yield file_path
    os.remove(file_path)

@pytest.fixture
def sample_docx():
    """Creates a temporary sample DOCX file for testing."""
    file_path = "test_sample.docx"
    with open(file_path, "wb") as f:
        f.write(b"This is a test DOCX content.")
    yield file_path
    os.remove(file_path)

@pytest.fixture
def mock_mongo_client():
    """Creates a mock MongoDB client."""
    return MongoClient()

@patch("app.config.client")
def test_chatbot_query(mock_mongo):
    """Test chatbot query with mocked MongoDB."""
    mock_mongo.return_value = mock_mongo_client
    with patch("app.services.llm_analysis.analyze_query", return_value={"skills": {"$regex": "Python", "$options": "i"}}):
        response = client.get("/chatbot/?query=Find candidates with Python skills")
    assert response.status_code == 200
    assert "query" in response.json()
    assert response.json()["query"] == "Find candidates with Python skills"
    assert "results" in response.json()

@patch("app.config.client")
def test_chatbot_query_no_results(mock_mongo):
    """Test chatbot query with a skill that doesn't exist in database."""
    mock_mongo.return_value = mock_mongo_client
    with patch("app.services.llm_analysis.analyze_query", return_value={"skills": {"$regex": "PYTHON", "$options": "i"}}):
        response = client.get("/chatbot/?query=Find candidates with PYTHON skills")
    assert response.status_code == 200
    assert "query" in response.json()
    assert response.json()["query"] == "Find candidates with PYTHON skills"
    assert "results" in response.json()
    assert response.json()["results"] == []
