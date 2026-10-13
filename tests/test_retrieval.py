from app.services.indexing_service import index_document
from app.services.retrieval_service import retrieve
from app.storage.vector_storage import VectorStore


def test_retrieval(tmp_path):
    # 1. Создаём документ
    file_path = tmp_path / "hr_policy.md"

    text = "Employees have 20 days of annual leave."
    file_path.write_text(text, encoding="utf-8")

    print("\n=== STEP 1: DOCUMENT ===")
    print("Document:", text)

    # 2. Создаём Vector Store
    store = VectorStore()

    # 3. Индексируем документ
    count = index_document(
        file_path=str(file_path),
        document_id="doc_001",
        owner_group="hr",
        store=store
    )

    print("\n=== STEP 2: INDEXING ===")
    print("Chunks indexed:", count)
    print("Stored chunks:", len(store.chunks))
    print("Embedding dimensions:", len(store.chunks[0]["embedding"]))
    print("First 5 embedding values:", store.chunks[0]["embedding"][:5])

    # 4. Задаём вопрос
    question = "How many vacation days do employees have?"

    print("\n=== STEP 3: USER QUESTION ===")
    print("Question:", question)

    # 5. Выполняем поиск
    results = retrieve(
        question=question,
        allowed_groups={"hr"},
        store=store,
        top_k=3
    )

    print("\n=== STEP 4: SEARCH RESULTS ===")

    for item in results:
        print("Text:", item["chunk"]["text"])
        print("Similarity:", round(item["score"], 4))
        print("Owner group:", item["chunk"]["owner_group"])

    # 6. Проверяем права доступа
    forbidden_results = retrieve(
        question=question,
        allowed_groups={"procurement"},
        store=store
    )

    print("\n=== STEP 5: SECURITY CHECK ===")
    print("Results for procurement:", forbidden_results)

    # 7. Проверяем правильность
    assert count == 1
    assert len(results) == 1
    assert results[0]["chunk"]["text"] == text
    assert forbidden_results == []


def test_multiple_documents(tmp_path):
    documents = [
        (
            "hr_policy.md",
            "Employees receive 20 days of paid annual leave.",
            "hr"
        ),
        (
            "it_policy.md",
            "Employees must change their passwords every 90 days.",
            "it"
        ),
        (
            "procurement_policy.md",
            "New laptops must be approved by the procurement department.",
            "procurement"
        )
    ]

    store = VectorStore()

    for filename, text, group in documents:
        file_path = tmp_path / filename
        file_path.write_text(text, encoding="utf-8")

        index_document(
            file_path=str(file_path),
            document_id=filename,
            owner_group=group,
            store=store
        )

    question = "How often should I update my password?"

    results = retrieve(
        question=question,
        allowed_groups={"hr", "it"},
        store=store,
        top_k=3
    )

    print("\n=== SEARCH RESULTS ===")
    print("Question:", question)

    for i, item in enumerate(results, start=1):
        print(f"\nResult #{i}")
        print("Document:", item["chunk"]["filename"])
        print("Group:", item["chunk"]["owner_group"])
        print("Score:", round(item["score"], 4))
        print("Text:", item["chunk"]["text"])

    assert len(store.chunks) == 3
    assert results[0]["chunk"]["filename"] == "it_policy.md"
    assert all(
        item["chunk"]["owner_group"] in {"hr", "it"}
        for item in results
    )
