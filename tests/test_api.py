
from app.core.auth import create_access_token


def auth_headers(username):
    token = create_access_token(username)
    return {"Authorization": f"Bearer {token}"}


def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_readiness_endpoint(client):
    response = client.get("/ready")
    assert response.status_code == 200
    assert response.json()["status"] == "ready"


def test_create_and_list_document(client):
    headers = auth_headers("alice")

    created = client.post(
        "/api/v1/documents",
        headers=headers,
        json={
            "title": "Procurement rules",
            "content": "Purchases above $10000 require director approval.",
            "owner_group": "procurement"
        }
    )

    assert created.status_code == 200

    listed = client.get(
        "/api/v1/documents",
        headers=headers
    )

    assert listed.status_code == 200
    assert any(
        d["title"] == "Procurement rules"
        for d in listed.json()
    )


def test_document_rejects_empty_content(client):
    response = client.post(
        "/api/v1/documents",
        headers=auth_headers("bob"),
        json={
            "title": "Empty",
            "content": "",
            "owner_group": "hr"
        }
    )

    assert response.status_code == 422


def test_documents_require_authentication(client):
    response = client.get("/api/v1/documents")

    assert response.status_code in (401, 403)
