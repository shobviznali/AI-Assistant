from app.models.schemas import ChatRequest
from app.services.chat_service import answer_question
from app.storage.vector_storage import store
from app.services.chunking_service import create_chunks
from app.services.embedding_service import generate_chunk_embeddings


def test_unauthorized_user():
    # 1. Очищаем Vector Store перед тестом
    store.chunks.clear()

    # 2. Создаём HR-документ
    chunks = create_chunks(
        document_id="hr-test-001",
        filename="hr_policy.md",
        text="Employees receive 20 days of paid annual leave.",
        owner_group="hr"
    )

    # 3. Генерируем embeddings
    embadding_chunks = generate_chunk_embeddings(chunks)

    # 4. Добавляем чанки в store
    store.add_chunks(embadding_chunks)

    # 5. Создаём ChatRequest от alice
    payload = ChatRequest(
        username="alice",
        question="How many vacation days do employees receive?"
    )

    # 6. Вызываем answer_question()
    answer = answer_question(payload)

    # 7. Проверяем результат
    assert answer.abstained is True
    assert answer.citations == []


def test_authorized_user():
    store.chunks.clear()

    # 2. Создаём HR-документ
    chunks = create_chunks(
        document_id="hr-test-001",
        filename="hr_policy.md",
        text="Employees receive 20 days of paid annual leave.",
        owner_group="hr"
    )

    # 3. Генерируем embeddings
    embadding_chunks = generate_chunk_embeddings(chunks)

    # 4. Добавляем чанки в store
    store.add_chunks(embadding_chunks)

    # 5. Создаём ChatRequest от alice
    payload = ChatRequest(
        username="bob",
        question="How many vacation days do employees receive?"
    )

    # 6. Вызываем answer_question()
    answer = answer_question(payload)

    # 7. Проверяем результат
    assert answer.abstained is False
    assert "20" in answer.answer
    assert answer.citations != []
