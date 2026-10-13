
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.core.auth import create_access_token


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def alice_headers():
    token = create_access_token("alice")
    return {
        "Authorization": f"Bearer {token}"
    }


@pytest.fixture
def bob_headers():
    token = create_access_token("bob")
    return {
        "Authorization": f"Bearer {token}"
    }
