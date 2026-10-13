from app.core.auth import create_access_token, verify_access_token
from app.core.password import  verify_password, hash_password
import pytest
from datetime import datetime, timedelta, timezone
import jwt
from dotenv import load_dotenv
import os

load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = "HS256"


def test_jwt():
    token = create_access_token("bob")
    username = verify_access_token(token)

    print("Decoded username:", username)

    assert username == "bob"


def test_invalid_token():
    with pytest.raises(ValueError, match="Invalid token"):
        verify_access_token("fake.jwt.token")


def test_expired_token():
    expired_time = datetime.now(timezone.utc) - timedelta(minutes=5)

    token = jwt.encode({"sub": "bob", "exp": expired_time}, JWT_SECRET, JWT_ALGORITHM)

    with pytest.raises(ValueError, match="Token has expired"):
        verify_access_token(token)


def test_correct_password():
    hashed_password = hash_password("secret123")

    assert verify_password("secret123", hashed_password) is True


def test_wrong_password():
    hashed_password = hash_password("secret123")

    assert verify_password("secret1234", hashed_password) is False

