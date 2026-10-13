
from fastapi import APIRouter, Depends, HTTPException, status

from app.models.schemas import (
    ChatRequest,
    ChatResponse,
    DocumentCreate,
    DocumentInfo,
    AuthenticatedChatRequest,
    LoginRequest,
)

from app.services.chat_service import answer_question
from app.services.document_service import (
    add_document,
    list_documents,
    get_document_for_user,
)

from app.core.auth import (
    get_current_user,
    authenticate_user,
    create_access_token,
)
from app.core.security import user_can_access


router = APIRouter()


# Create document
@router.post("/documents", response_model=DocumentInfo)
def create_document(
    payload: DocumentCreate,
    username: str = Depends(get_current_user),
):
    if not user_can_access(username, payload.owner_group):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
        )

    return add_document(payload)


# List accessible documents
@router.get("/documents", response_model=list[DocumentInfo])
def documents(
    username: str = Depends(get_current_user),
):
    return list_documents(username)


# Get document by ID
@router.get("/documents/{document_id}", response_model=DocumentInfo)
def document_details(
    document_id: str,
    username: str = Depends(get_current_user),
):
    doc = get_document_for_user(document_id, username)

    if doc is None:
        # Do not disclose whether a forbidden document exists.
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found",
        )

    return doc


# Chat with AI
@router.post("/chat", response_model=ChatResponse)
def chat(
    payload: ChatRequest,
    username: str = Depends(get_current_user),
):
    authenticated_payload = AuthenticatedChatRequest(
        username=username,
        question=payload.question,
    )

    return answer_question(authenticated_payload)


# Login
@router.post("/login")
def login(payload: LoginRequest):
    if not authenticate_user(payload.username, payload.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    token = create_access_token(payload.username)

    return {
        "access_token": token,
        "token_type": "bearer",
    }
