from app.services.chunking_service import create_chunks


def test_create_chunks():
    result = create_chunks(
        document_id="doc_001",
        filename="policy.md",
        text="A" * 900,
        owner_group="hr",
        chunk_size=500,
        overlap=100
    )

    assert result[0]["document_id"] == "doc_001"
    assert len(result) == 2
    assert result[1]["chunk_index"] == 1
    assert result[0]["owner_group"] == 'hr'
    assert result[1]["owner_group"] == 'hr'
    assert len(result[0]["text"]) == 500
    assert len(result[1]["text"]) == 500
