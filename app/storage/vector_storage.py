import numpy as np


class VectorStore:
    def __init__(self):
        self.chunks = []

    def add_chunks(self, chunks: list[dict]) -> None:

        self.chunks.extend(chunks)

    def search(self, query_embedding: list[float], allowed_groups: set[str], top_k: int = 3) -> list[dict]:

        if top_k <= 0:
            raise ValueError("top_k must be greater than zero")
        result = []
        for chunk in self.chunks:
            if chunk["owner_group"] in allowed_groups:
                score = cosine_similarity(query_embedding, chunk["embedding"])
                result.append({
                    "chunk": chunk,
                    "score": score
                })

        result = sorted(result, key = lambda item: item["score"], reverse=True)

        result = result[:top_k]

        return result


def cosine_similarity(a: list[float], b: list[float]) -> float:
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)

    if norm_a == 0 or norm_b == 0:
        raise ValueError("Vector length cannot be zero")
    if len(a) != len(b):
        raise ValueError("Vectors must have the same dimensions")

    result = np.dot(a, b) / (norm_a * norm_b)

    return float(result)


store = VectorStore()
