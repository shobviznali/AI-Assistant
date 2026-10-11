from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")


def generate_embedding(text: str) -> list[float]:
    embedding = model.encode(text)

    return embedding.tolist()


def generate_chunk_embeddings(chunks: list[dict]) -> list[dict]:

    for i in range(len(chunks)):
        chunks[i]["embedding"] = generate_embedding(chunks[i]["text"])

    return chunks
