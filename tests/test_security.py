
from app.core.auth import create_access_token


def auth_headers(username):
    token = create_access_token(username)
    return {"Authorization": f"Bearer {token}"}


def create_document(client, username, title, content, group):
    return client.post(
        "/api/v1/documents",
        headers=auth_headers(username),
        json={
            "title": title,
            "content": content,
            "owner_group": group
        }
    )


def test_alice_sees_procurement_but_not_hr(client):
    procurement = create_document(
        client, "alice", "Procurement secret",
        "Tender details", "procurement"
    )

    hr = create_document(
        client, "bob", "HR secret",
        "Salary details", "hr"
    )

    assert procurement.status_code == 200
    assert hr.status_code == 200

    response = client.get(
        "/api/v1/documents",
        headers=auth_headers("alice")
    )

    assert response.status_code == 200

    titles = {item["title"] for item in response.json()}

    assert "Procurement secret" in titles
    assert "HR secret" not in titles


def test_bob_sees_hr_but_not_procurement(client):
    procurement = create_document(
        client, "alice", "Procurement secret",
        "Tender details", "procurement"
    )

    hr = create_document(
        client, "bob", "HR secret",
        "Salary details", "hr"
    )

    assert procurement.status_code == 200
    assert hr.status_code == 200

    response = client.get(
        "/api/v1/documents",
        headers=auth_headers("bob")
    )

    assert response.status_code == 200

    titles = {item["title"] for item in response.json()}

    assert "HR secret" in titles
    assert "Procurement secret" not in titles


def test_unauthorized_document_lookup_returns_not_found(client):
    created = create_document(
        client, "bob", "HR secret",
        "Salary details", "hr"
    )

    assert created.status_code == 200

    document_id = created.json()["id"]

    response = client.get(
        f"/api/v1/documents/{document_id}",
        headers=auth_headers("alice")
    )

    assert response.status_code == 404


def test_alice_cannot_create_hr_document(client):
    response = create_document(
        client, "alice", "Forbidden HR document",
        "Private HR information", "hr"
    )

    assert response.status_code == 403


def test_bob_cannot_create_procurement_document(client):
    response = create_document(
        client, "bob", "Forbidden procurement document",
        "Private procurement information", "procurement"
    )

    assert response.status_code == 403


def test_unknown_user_has_no_documents(client):
    create_document(
        client, "bob", "HR secret",
        "Salary details", "hr"
    )

    response = client.get(
        "/api/v1/documents",
        headers=auth_headers("mallory")
    )

    assert response.status_code == 200
    assert response.json() == []
