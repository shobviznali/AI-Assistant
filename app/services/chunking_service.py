def split_text(text: str, chunk_size: int, overlap: int) -> list[str]:
    validate_chunk_params(chunk_size, overlap)

    chunks = []
    start = 0

    while start < len(text):
        chunks.append(text[start:start+chunk_size])
        if start + chunk_size >= len(text):
            break
        start += chunk_size - overlap
    return chunks


def create_chunks(document_id: str, filename: str, text: str, owner_group: str, chunk_size: int = 500, overlap: int = 100) -> list[dict]:

    chunks = split_text(text, chunk_size, overlap)
    result = []

    for i, value in enumerate(chunks):
        chunk_data = {
            "document_id": document_id,
            "filename": filename,
            "chunk_index": i,
            "owner_group": owner_group,
            "text": value
        }
        result.append(chunk_data)

    return result


def validate_chunk_params(chunk_size: int, overlap: int) -> None:
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")
    if overlap < 0:
        raise ValueError("overlap must be possitive")
    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")
