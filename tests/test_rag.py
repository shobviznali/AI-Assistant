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
