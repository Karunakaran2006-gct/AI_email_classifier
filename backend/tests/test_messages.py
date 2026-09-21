from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_create_message():
    response = client.post(
        "/api/messages/",
        json={
            "sender": "test@example.com",
            "subject": "Test message",
            "body": "This is a test message."
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["sender"] == "test@example.com"
    assert data["subject"] == "Test message"
    assert "id" in data


def test_get_messages():
    response = client.get("/api/messages/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_missing_message():
    response = client.get("/api/messages/999999")

    assert response.status_code == 404


def test_summary():
    response = client.get("/api/messages/summary")

    assert response.status_code == 200

    data = response.json()

    assert "total_messages" in data
    assert "by_category" in data
    assert "by_priority" in data


def test_filter_by_priority():
    response = client.get(
        "/api/messages/",
        params={"priority": "High"}
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_filter_by_category():
    response = client.get(
        "/api/messages/",
        params={"category": "Complaint"}
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)