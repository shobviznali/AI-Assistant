from app.models.schemas import ChatRequest, ChatResponse, AuthenticatedChatRequest
from app.services.retrieval_service import retrieve
from app.services.prompt_service import build_prompt
from app.services.llm_service import generate_answer
from app.core.security import USER_GROUPS
from app.storage.vector_storage import store


def answer_question(payload: ChatRequest) -> ChatResponse:
    allowed_groups = USER_GROUPS.get(payload.username.lower(), set())
    chunks = retrieve(payload.question, allowed_groups, store)

    if not chunks:
        return ChatResponse(
            answer="I don't have enough information in the accessible documents to answer that.",
            citations=[],
            abstained=True,
        )

    prompt = build_prompt(payload.question, chunks)
    answer = generate_answer(prompt)

    citations = [
        {
            "document_id": c["chunk"]["document_id"],
            "title": c["chunk"]["filename"],
            "excerpt": c["chunk"]["text"]
        }
        for c in chunks
    ]
    return ChatResponse(
        answer=answer,
        citations=citations,
        abstained=False,
    )
