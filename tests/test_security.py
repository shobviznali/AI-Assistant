def test_alice_sees_procurement_but_not_hr(client):
    client.post("/api/v1/documents", json={
        "title": "Procurement secret", "content": "Tender details", "owner_group": "procurement"
    })
    client.post("/api/v1/documents", json={
        "title": "HR secret", "content": "Salary details", "owner_group": "hr"
    })
    response = client.get("/api/v1/documents", params={"username": "alice"})
    assert response.status_code == 200
    titles = {item["title"] for item in response.json()}
    assert "Procurement secret" in titles
    assert "HR secret" not in titles

def test_bob_sees_hr_but_not_procurement(client):
    client.post("/api/v1/documents", json={
        "title": "Procurement secret", "content": "Tender details", "owner_group": "procurement"
    })
    client.post("/api/v1/documents", json={
        "title": "HR secret", "content": "Salary details", "owner_group": "hr"
    })
    response = client.get("/api/v1/documents", params={"username": "bob"})
    assert response.status_code == 200
    titles = {item["title"] for item in response.json()}
    assert "HR secret" in titles
    assert "Procurement secret" not in titles

def test_unauthorized_document_lookup_returns_not_found(client):
    created = client.post("/api/v1/documents", json={
        "title": "HR secret", "content": "Salary details", "owner_group": "hr"
    }).json()
    response = client.get(f"/api/v1/documents/{created['id']}", params={"username": "alice"})
    assert response.status_code == 404

def test_unknown_user_has_no_documents(client):
    client.post("/api/v1/documents", json={
        "title": "HR secret", "content": "Salary details", "owner_group": "hr"
    })
    response = client.get("/api/v1/documents", params={"username": "mallory"})
    assert response.status_code == 200
    assert response.json() == []
