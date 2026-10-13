"""Retrieval TODO.

Implement chunking and retrieval here. Always filter documents by the
requesting user's permissions BEFORE searching/ranking chunks.
"""
from app.services.embedding_service import generate_embedding
from app.storage.vector_storage import VectorStore


def retrieve(
    question: str,
    allowed_groups: set[str],
    store: VectorStore,
    top_k: int = 3
) -> list[dict]:
    query_embedding = generate_embedding(question)
    result = store.search(query_embedding, allowed_groups, top_k)

    return result


def retrieve_relevant_chunks(question: str, username: str) -> list[dict]:
    # TODO: return relevant authorized chunks with document_id/title/excerpt.
    return []
