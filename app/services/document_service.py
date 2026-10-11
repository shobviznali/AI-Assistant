"""Temporary in-memory document store for the starter project.

TODO for the assignment:
- Persist documents / build an index.
- Store filename/page/chunk metadata.
- Validate size and content type.
- Add pagination and robust error handling.
"""
from uuid import uuid4
from app.core.security import user_can_access
from app.models.schemas import DocumentCreate, DocumentInfo
from pathlib import Path
from app.services.chunking_service import create_chunks

_DOCUMENTS: dict[str, dict] = {}

def add_document(payload: DocumentCreate) -> DocumentInfo:
    document_id = str(uuid4())
    item = {
        "id": document_id,
        "title": payload.title,
        "content": payload.content,
        "owner_group": payload.owner_group,
    }
    _DOCUMENTS[document_id] = item
    return DocumentInfo(id=document_id, title=item["title"], owner_group=item["owner_group"])

def list_documents(username: str) -> list[DocumentInfo]:
    return [
        DocumentInfo(id=d["id"], title=d["title"], owner_group=d["owner_group"])
        for d in _DOCUMENTS.values()
        if user_can_access(username, d["owner_group"])
    ]

def get_document_for_user(document_id: str, username: str):
    item = _DOCUMENTS.get(document_id)
    if not item or not user_can_access(username, item["owner_group"]):
        return None
    return DocumentInfo(id=item["id"], title=item["title"], owner_group=item["owner_group"])


def read_document(file_path: str) -> str:
    path = Path(file_path)
    if not path.exists() or not path.is_file():
        raise ValueError("Path doesn't exist or it's not a file")
    if path.suffix.lower() not in (".md", ".txt"):
        raise ValueError("File should be txt or md format")
    content = path.read_text(encoding='utf-8')

    return content


def clean_text(text):
    pass


def process_document(file_path: str, document_id: str, owner_group: str, chunk_size: int = 500, overlap: int = 100) -> list[dict]:
    path = Path(file_path)
    text = read_document(str(path))
    result = create_chunks(document_id, path.name, text, owner_group, chunk_size, overlap)

    return result

def _get_all_for_testing():
    return _DOCUMENTS

def _reset_for_testing():
    _DOCUMENTS.clear()

