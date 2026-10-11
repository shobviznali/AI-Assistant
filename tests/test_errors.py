def test_reject_invalid_owner_group(client):
    response = client.post("/api/v1/documents", json={
        "title": "Bad group", "content": "text", "owner_group": "everyone"
    })
    assert response.status_code == 422

def test_reject_missing_username_for_document_list(client):
    response = client.get("/api/v1/documents")
    assert response.status_code == 422

def test_reject_blank_chat_question(client):
    response = client.post("/api/v1/chat", json={
        "username": "alice", "question": "   "
    })
    # Whitespace-only validation is a TODO; current schema may accept this.
    assert response.status_code == 422

def test_reject_oversized_document(client):
    huge_content = "x" * 100_001
    response = client.post("/api/v1/documents", json={
        "title": "Too large", "content": huge_content, "owner_group": "hr"
    })
    assert response.status_code == 422
