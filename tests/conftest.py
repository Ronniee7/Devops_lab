from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client() -> Iterator[TestClient]:
    """
    Provide a test client for API endpoint testing.
    """

    with TestClient(app) as test_client:
        yield test_client
