from fastapi import APIRouter, HTTPException
from app.models.schemas import ChatRequest, ChatResponse, DocumentCreate, DocumentInfo
from app.services.chat_service import answer_question
from app.services.document_service import add_document, list_documents, get_document_for_user

router = APIRouter()

@router.post("/documents", response_model=DocumentInfo)
def create_document(payload: DocumentCreate):
    return add_document(payload)

@router.get("/documents", response_model=list[DocumentInfo])
def documents(username: str):
    return list_documents(username)

@router.get("/documents/{document_id}", response_model=DocumentInfo)
def document_details(document_id: str, username: str):
    doc = get_document_for_user(document_id, username)
    if doc is None:
        # Do not disclose whether a forbidden document exists.
        raise HTTPException(status_code=404, detail="Document not found")
    return doc

@router.post("/chat", response_model=ChatResponse)
def chat(payload: ChatRequest):
    return answer_question(payload)
