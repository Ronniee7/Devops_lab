from datetime import datetime

from fastapi.testclient import TestClient

from app.core.config import settings


def test_root_endpoint(client: TestClient):
    response = client.get("/")

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/json")

    data = response.json()

    assert data["message"] == "Welcome to DevOps Lab"
    assert data["application"] == settings.APP_NAME
    assert data["version"] == settings.APP_VERSION
    assert data["environment"] == settings.APP_ENV
    assert data["status"] == "running"


def test_health_endpoint(client: TestClient):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/json")

    data = response.json()

    assert data["status"] == "healthy"
    assert data["environment"] == settings.APP_ENV

    timestamp = datetime.fromisoformat(data["timestamp"])

    assert timestamp.tzinfo is not None


def test_unknown_endpoint_returns_404(client: TestClient):
    response = client.get("/unknown-endpoint")

    assert response.status_code == 404
    assert response.json()["detail"] == "Not Found"


def test_openapi_documentation(client: TestClient):
    response = client.get("/openapi.json")

    assert response.status_code == 200

    data = response.json()

    assert data["info"]["title"] == settings.APP_NAME
    assert data["info"]["version"] == settings.APP_VERSION


def test_root_rejects_unsupported_method(client: TestClient):
    response = client.post("/")

    assert response.status_code == 405


def test_health_rejects_unsupported_method(client: TestClient):
    response = client.post("/health")

    assert response.status_code == 405