def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_readiness_endpoint(client):
    response = client.get("/ready")
    assert response.status_code == 200
    assert response.json()["status"] == "ready"

def test_create_and_list_document(client):
    created = client.post("/api/v1/documents", json={
        "title": "Procurement rules",
        "content": "Purchases above $10000 require director approval.",
        "owner_group": "procurement"
    })
    assert created.status_code == 200
    listed = client.get("/api/v1/documents", params={"username": "alice"})
    assert listed.status_code == 200
    assert any(d["title"] == "Procurement rules" for d in listed.json())

def test_document_rejects_empty_content(client):
    response = client.post("/api/v1/documents", json={
        "title": "Empty", "content": "", "owner_group": "hr"
    })
    assert response.status_code == 422
