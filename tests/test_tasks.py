from fastapi.testclient import TestClient
from sqlalchemy.exc import SQLAlchemyError

from app.db.session import get_db
from app.main import app


def test_task_crud_lifecycle(client: TestClient):
    # Create
    response = client.post(
        "/api/v1/tasks/",
        json={
            "title": "Complete CI pipeline",
            "description": "Add meaningful automated tests",
        },
    )

    assert response.status_code == 201
    created = response.json()

    task_id = created["id"]

    assert created["title"] == "Complete CI pipeline"
    assert created["description"] == "Add meaningful automated tests"
    assert created["status"] == "pending"
    assert created["created_at"]

    # Retrieve
    response = client.get(f"/api/v1/tasks/{task_id}")

    assert response.status_code == 200
    assert response.json()["id"] == task_id

    # List
    response = client.get("/api/v1/tasks/")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["id"] == task_id

    # Update
    response = client.patch(
        f"/api/v1/tasks/{task_id}",
        json={
            "title": "CI pipeline completed",
            "status": "completed",
        },
    )

    assert response.status_code == 200
    updated = response.json()

    assert updated["title"] == "CI pipeline completed"
    assert updated["status"] == "completed"
    assert updated["description"] == "Add meaningful automated tests"

    # Delete
    response = client.delete(f"/api/v1/tasks/{task_id}")

    assert response.status_code == 204

    # Confirm deletion
    response = client.get(f"/api/v1/tasks/{task_id}")

    assert response.status_code == 404


def test_create_task_without_description(client: TestClient):
    response = client.post(
        "/api/v1/tasks/",
        json={"title": "Task without description"},
    )

    assert response.status_code == 201
    assert response.json()["description"] is None


def test_create_task_rejects_empty_title(client: TestClient):
    response = client.post(
        "/api/v1/tasks/",
        json={"title": ""},
    )

    assert response.status_code == 422


def test_create_task_rejects_title_over_200_characters(
    client: TestClient,
):
    response = client.post(
        "/api/v1/tasks/",
        json={"title": "x" * 201},
    )

    assert response.status_code == 422


def test_update_task_rejects_invalid_status(client: TestClient):
    create_response = client.post(
        "/api/v1/tasks/",
        json={"title": "Validate task status"},
    )

    task_id = create_response.json()["id"]

    response = client.patch(
        f"/api/v1/tasks/{task_id}",
        json={"status": "invalid"},
    )

    assert response.status_code == 422


def test_list_tasks_returns_empty_list(client: TestClient):
    response = client.get("/api/v1/tasks/")

    assert response.status_code == 200
    assert response.json() == []


def test_get_missing_task_returns_404(client: TestClient):
    response = client.get("/api/v1/tasks/9999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


def test_update_missing_task_returns_404(client: TestClient):
    response = client.patch(
        "/api/v1/tasks/9999",
        json={"title": "Updated title"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


def test_delete_missing_task_returns_404(client: TestClient):
    response = client.delete("/api/v1/tasks/9999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


def test_create_task_rolls_back_on_database_error(client: TestClient):
    class FailingSession:
        rollback_called = False

        def add(self, task):
            pass

        def commit(self):
            raise SQLAlchemyError("Simulated database failure")

        def rollback(self):
            self.rollback_called = True

        def refresh(self, task):
            pass

    failing_session = FailingSession()

    def override_get_db():
        yield failing_session

    app.dependency_overrides[get_db] = override_get_db

    try:
        response = client.post(
            "/api/v1/tasks/",
            json={"title": "This operation should fail"},
        )
    finally:
        app.dependency_overrides.pop(get_db, None)

    assert response.status_code == 503
    assert response.json() == {"detail": "A database operation could not be completed."}
    assert failing_session.rollback_called is True
