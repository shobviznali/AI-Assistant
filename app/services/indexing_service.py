from app.services.document_service import process_document
from app.services.embedding_service import generate_chunk_embeddings
from app.storage.vector_storage import VectorStore


def index_document(
    file_path: str,
    document_id: str,
    owner_group: str,
    store: VectorStore
) -> int:
    res = process_document(file_path, document_id, owner_group)
    chunk = generate_chunk_embeddings(res)
    store.add_chunks(chunk)

    return len(res)