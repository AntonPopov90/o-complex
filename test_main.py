"""module for testing"""

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_read_main():
    """test main page coonnection"""
    response = client.get('/')
    assert response.status_code == 200
    assert response.charset_encoding == 'utf-8'

