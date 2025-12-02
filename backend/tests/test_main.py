from fastapi.testclient import TestClient
from unittest.mock import patch
import sys
import os

# Add the parent directory to sys.path to import backend modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Culture AI Project is running."}

@patch("main.answer_question")
def test_ask_endpoint(mock_answer_question):
    # Mock the answer_question function to return a specific response
    mock_answer_question.return_value = "This is a mocked answer."
    
    question = "What is culture?"
    response = client.get(f"/ask?q={question}")
    
    assert response.status_code == 200
    assert response.json() == {"question": question, "answer": "This is a mocked answer."}
    
    # Verify that the mock was called with the correct argument
    mock_answer_question.assert_called_once_with(question)

@patch("main.answer_question")
def test_ask_endpoint_error(mock_answer_question):
    # Mock the answer_question function to raise an exception
    mock_answer_question.side_effect = Exception("Something went wrong")
    
    question = "Error question"
    response = client.get(f"/ask?q={question}")
    
    assert response.status_code == 500
    assert response.json() == {"detail": "Something went wrong"}
