import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services.document_service import _reset_for_testing

@pytest.fixture()
def client():
    _reset_for_testing()
    return TestClient(app)
