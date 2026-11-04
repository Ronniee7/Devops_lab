
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["status"] == "running"


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_readiness_endpoint():
    response = client.get("/ready")

    assert response.status_code == 200
    assert response.json()["ready"] is True


def test_info_endpoint():
    response = client.get("/info")

    assert response.status_code == 200
    assert response.json()["name"] == "DevOps Lab API"


def test_version_endpoint():
    response = client.get("/version")

    assert response.status_code == 200
    assert response.json()["version"] == "0.2.0"


def test_metrics_endpoint():
    response = client.get("/metrics")

    assert response.status_code == 200
    assert "uptime_seconds" in response.json()
    assert "total_requests" in response.json()


def test_echo_endpoint():
    response = client.post(
        "/echo",
        json={
            "message": "Hello DevOps",
            "metadata": {"environment": "test"},
        },
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Hello DevOps"


def test_echo_rejects_empty_message():
    response = client.post(
        "/echo",
        json={"message": ""},
    )

    assert response.status_code == 422


def test_request_id_header():
    response = client.get("/health")

    assert "X-Request-ID" in response.headers
