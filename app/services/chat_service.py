from app.models.schemas import ChatRequest, ChatResponse
from app.services.retrieval_service import retrieve_relevant_chunks

def answer_question(payload: ChatRequest) -> ChatResponse:
    chunks = retrieve_relevant_chunks(payload.question, payload.username)
    if not chunks:
        return ChatResponse(
            answer="I don't have enough information in the accessible documents to answer that.",
            citations=[],
            abstained=True,
        )

    # TODO: call generate_answer() with the retrieved context.
    # TODO: verify citations are limited to the retrieved authorized chunks.
    citations = [
        {"document_id": c["document_id"], "title": c["title"], "excerpt": c["excerpt"]}
        for c in chunks
    ]
    return ChatResponse(
        answer="TODO: generate a grounded answer from the retrieved context.",
        citations=citations,
        abstained=False,
    )
