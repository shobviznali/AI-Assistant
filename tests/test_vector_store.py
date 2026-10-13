from app.storage.vector_storage import cosine_similarity
from pytest import approx, raises
from app.storage.vector_storage import VectorStore


def test_cosine_similarity():
    assert cosine_similarity([1, 0], [1, 0]) == approx(1.0)
    assert cosine_similarity([1, 0], [0, 1]) == approx(0.0)

    with raises(ValueError):
        cosine_similarity([1, 0], [0, 0])


def test_vector_store_search():
    store = VectorStore()

    store.add_chunks([
        {
            "text": "Vacation policy",
            "owner_group": "hr",
            "embedding": [1.0, 0.0]
        },
        {
            "text": "Salary policy",
            "owner_group": "hr",
            "embedding": [0.8, 0.6]
        },
        {
            "text": "Procurement secrets",
            "owner_group": "procurement",
            "embedding": [1.0, 0.0]
        }
    ])

    res = store.search(query_embedding=[1.0, 0.0], allowed_groups={"hr"}, top_k=2)

    assert len(res) == 2
    assert res[0]["chunk"]["text"] == "Vacation policy"
    assert all(
        item["chunk"]["owner_group"] != "procurement"
        for item in res
    )
