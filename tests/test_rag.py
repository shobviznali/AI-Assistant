from app.storage.vector_storage import VectorStore
from app.services.indexing_service import index_document
from app.services.retrieval_service import retrieve
from app.services.prompt_service import build_prompt
from app.services.llm_service import generate_answer


def test_chat_abstains_when_no_authorized_evidence(client):
    response = client.post("/api/v1/chat", json={
        "username": "alice", "question": "What is the employee vacation policy?"
    })
    assert response.status_code == 200
    body = response.json()
    assert body["abstained"] is True
    assert body["citations"] == []

def test_chat_response_has_expected_shape(client):
    response = client.post("/api/v1/chat", json={
        "username": "alice", "question": "What are the procurement rules?"
    })
    assert response.status_code == 200
    body = response.json()
    assert isinstance(body["answer"], str)
    assert isinstance(body["citations"], list)
    assert isinstance(body["abstained"], bool)

def test_chat_does_not_return_hr_citations_to_alice(client):
    client.post("/api/v1/documents", json={
        "title": "HR confidential", "content": "The payroll code is 12345.", "owner_group": "hr"
    })
    response = client.post("/api/v1/chat", json={
        "username": "alice", "question": "What is the payroll code?"
    })
    assert response.status_code == 200
    assert all(c["title"] != "HR confidential" for c in response.json()["citations"])


def test_rag_pipeline(tmp_path):
    # 1. Создаём тестовый документ
    file_path = tmp_path / "hr_policy.md"

    file_path.write_text(
        "Employees receive 20 days of paid annual leave.",
        encoding="utf-8"
    )

    # 2. Создаём Vector Store
    store = VectorStore()

    # 3. Индексируем документ
    index_document(
        file_path=str(file_path),
        document_id="hr-001",
        owner_group="hr",
        store=store
    )

    # 4. Задаём вопрос
    question = "How many paid vacation days do employees receive?"

    # 5. Ищем подходящие документы
    results = retrieve(
        question=question,
        allowed_groups={"hr"},
        store=store,
        top_k=3
    )

    # 6. Создаём prompt
    prompt = build_prompt(question, results)

    # 7. Отправляем в LLM
    answer = generate_answer(prompt)

    print("\n=== QUESTION ===")
    print(question)

    print("\n=== RETRIEVED DOCUMENTS ===")
    for item in results:
        print(item["chunk"]["filename"], item["score"])

    print("\n=== AI ANSWER ===")
    print(answer)

    assert len(results) > 0
    assert "20" in answer
