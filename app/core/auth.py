import os
import jwt
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pwdlib import PasswordHash
from app.core.users import USERS
from app.core.password import verify_password

password_hash = PasswordHash.recommended()

bearer_scheme = HTTPBearer()

load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = "HS256"


def create_access_token(username: str) -> str:
    time_now = datetime.now(timezone.utc)
    time_after_30_minutes = time_now + timedelta(minutes=30)

    payload = {"sub": username, "exp": time_after_30_minutes}
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token


def verify_access_token(token: str) -> str:
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload["sub"]

    except jwt.ExpiredSignatureError:
        raise ValueError("Token has expired")

    except jwt.InvalidTokenError:
        raise ValueError("Invalid token")


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
) -> str:
    token = credentials.credentials

    try:
        username = verify_access_token(token)
        return username
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e)) from e



def authenticate_user(username: str, password: str) -> bool:
    if username in USERS:
        return verify_password(password, USERS[username]["hashed_password"])

    return False
