from app.services.embedding_service import generate_embedding, generate_chunk_embeddings
from app.services.chunking_service import create_chunks

def test_generate_embedding():
    embedding = generate_embedding("Hello AI")

    assert isinstance(embedding, list)
    assert len(embedding) == 384
    assert isinstance(embedding[0], float)


def test_generate_chunk_embeddings():
    chunks = create_chunks(
        document_id="doc_001",
        filename="policy.md",
        text="A" * 900,
        owner_group="hr",
        chunk_size=500,
        overlap=100
    )

    original_texts = [chunk["text"] for chunk in chunks]

    result = generate_chunk_embeddings(chunks)

    assert len(result) == 2

    for chunk in result:
        assert "embedding" in chunk
        assert isinstance(chunk["embedding"], list)
        assert len(chunk["embedding"]) == 384
        assert all(isinstance(x, float) for x in chunk["embedding"])

    assert [chunk["text"] for chunk in result] == original_texts

    assert result[0]["document_id"] == "doc_001"
    assert result[0]["filename"] == "policy.md"
    assert result[0]["owner_group"] == "hr"
