from secrets import token_urlsafe
from typing import Self

from tests.api.experiment_recipes import create_experiment
from triangler_fastapi.schemas import ExperimentOutSchema

from .client import create_test_client


class TestExperimentsApiEndpoints:
    def test_create_experiment_succeeds(self: Self) -> None:
        # arrange
        test_name = f"test {token_urlsafe(8)}"
        client = create_test_client()

        # act
        test_experiment = create_experiment(client, name=test_name)

        # assert
        assert test_experiment.id is not None
        assert test_experiment.name == test_name

    def test_get_experiment_succeeds(self: Self) -> None:
        # arrange
        test_name = f"test {token_urlsafe(8)}"
        client = create_test_client()
        test_experiment = create_experiment(client, name=test_name)

        # act
        resp = client.get(f"/api/v1/experiments/{test_experiment.id}")
        assert resp.status_code == 200
        experiment_response_raw = resp.json()
        experiment = ExperimentOutSchema.model_validate(experiment_response_raw)

        # assert
        assert test_experiment.name == experiment.name
        assert test_experiment.id == experiment.id

    def test_get_experiment_not_exists(self: Self) -> None:
        # arrange
        non_existant_id = -1
        client = create_test_client()

        # act
        resp = client.get(f"/api/v1/experiments/{non_existant_id}")

        # assert
        assert resp.status_code == 404

    def test_get_all_experiments_succeeds(self: Self) -> None:
        # arrange
        test_name = f"test {token_urlsafe(8)}"
        client = create_test_client()
        _ = create_experiment(client, name=test_name)

        # act
        resp = client.get("/api/v1/experiments/")
        assert resp.status_code == 200
        all_experiments_raw = resp.json()
        all_experiments = [
            ExperimentOutSchema.model_validate(x) for x in all_experiments_raw
        ]

        # assert
        assert all_experiments
        assert test_name in [x.name for x in all_experiments]

    def test_update_experiment_succeeds(self: Self) -> None:
        # arrange
        test_name = f"test {token_urlsafe(8)}"
        client = create_test_client()
        test_experiment = create_experiment(client, name=test_name)

        # act
        resp = client.get(f"/api/v1/experiments/{test_experiment.id}")
        assert resp.status_code == 200
        experiment_response_raw = resp.json()
        experiment = ExperimentOutSchema.model_validate(experiment_response_raw)

        # assert
        assert test_experiment.name == experiment.name
        assert test_experiment.id == experiment.id

        # act
        test_new_name = f"test {token_urlsafe(8)}"
        experiment.name = test_new_name
        updated_experiment_data = experiment.model_dump_json(
            exclude={"id", "sample_size", "p_value", "created_at", "updated_at"}
        )
        resp_update = client.put(
            f"/api/v1/experiments/{test_experiment.id}", content=updated_experiment_data
        )
        assert resp_update.status_code == 200
        experiment_response_raw = resp.json()
        resp_updated_get = client.get(f"/api/v1/experiments/{test_experiment.id}")
        assert resp_updated_get.status_code == 200
        updated_experiment = ExperimentOutSchema.model_validate(resp_updated_get.json())

        # assert
        assert updated_experiment.name == test_new_name
        assert test_experiment.id == experiment.id

    def test_delete_experiment_succeeds(self: Self) -> None:
        # arrange
        test_name = f"test {token_urlsafe(8)}"
        client = create_test_client()
        test_experiment = create_experiment(client, name=test_name)

        # act
        resp = client.get(f"/api/v1/experiments/{test_experiment.id}")
        assert resp.status_code == 200
        experiment_response_raw = resp.json()
        experiment = ExperimentOutSchema.model_validate(experiment_response_raw)

        # assert
        assert test_experiment.name == experiment.name
        assert test_experiment.id == experiment.id

        # act
        resp_delete = client.delete(f"/api/v1/experiments/{test_experiment.id}")
        assert resp_delete.status_code == 200
        resp_delete_get = client.get(f"/api/v1/experiments/{test_experiment.id}")

        # assert
        assert resp_delete_get.status_code == 404
