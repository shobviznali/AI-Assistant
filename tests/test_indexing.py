from app.services.indexing_service import index_document
from app.storage.vector_storage import VectorStore


def test_index_document(tmp_path):
    file_path = tmp_path / "hr_policy.md"

    text = "Employees have 20 days of annual leave."

    file_path.write_text(text, encoding="utf-8")

    store = VectorStore()

    count = index_document(
        file_path=str(file_path),
        document_id="doc_001",
        owner_group="hr",
        store=store
    )

    assert count == 1
    assert len(store.chunks) == 1

    chunk = store.chunks[0]

    assert chunk["text"] == text
    assert chunk["document_id"] == "doc_001"
    assert chunk["owner_group"] == "hr"

    assert "embedding" in chunk
    assert len(chunk["embedding"]) == 384
