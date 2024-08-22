from fastapi.testclient import TestClient

from triangler_fastapi.main import app


def create_test_client() -> TestClient:
    return TestClient(app)
