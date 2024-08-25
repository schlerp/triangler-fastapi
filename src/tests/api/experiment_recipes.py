from datetime import datetime
from datetime import timedelta

from fastapi.testclient import TestClient

from triangler_fastapi.schemas import ExperimentOutSchema


def create_experiment(
    client: TestClient, name: str = "Test Experiment"
) -> ExperimentOutSchema:
    response = client.post(
        "/api/v1/experiments/",
        json={
            "name": name,
            "description": "This is a test experiment.",
            "start_on": datetime.today().date().isoformat(),
            "end_on": (datetime.today() + timedelta(days=7)).date().isoformat(),
            "observations": [],
        },
    )
    assert response.status_code == 201, response.text
    data = response.json()
    return ExperimentOutSchema.model_validate(data)
