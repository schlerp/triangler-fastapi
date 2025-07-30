from typing import Literal

from loguru import logger
from sqlalchemy.exc import NoResultFound

from triangler_fastapi.domain import schemas
from triangler_fastapi.domain.repositories import ExperimentRepository
from triangler_fastapi.domain.repositories import SampleFlightRepository
from triangler_fastapi.exceptions import errors


def get_sample_flight_by_id(
    *,
    sample_flight_id: int,
    sample_flight_repository: SampleFlightRepository,
) -> schemas.SampleFlightOutSchema:
    """Gets a sample flight by its id."""
    try:
        sample_flight = sample_flight_repository.get_by_id(id=sample_flight_id)
    except NoResultFound:
        error_message = f"Sample flight with id {sample_flight_id} not found."
        logger.error(error_message)
        raise errors.ObjectNotFoundError(error_message)
    return sample_flight


def create_new_sample_flight_for_experiment(
    *,
    experiment_id: int,
    experiment_repository: ExperimentRepository,
    sample_flight_repository: SampleFlightRepository,
    correct_sample: Literal["A", "B", "C"] | None = None,
) -> schemas.SampleFlightOutSchema:
    """Creates a new sample flight with no response for the specified experiment."""
    experiment = experiment_repository.get_by_id(id=experiment_id)
    if experiment is None:
        raise ValueError(f"Experiment with id {experiment_id} not found.")

    sample_flight_data = schemas.SampleFlightInSchema.new(
        experiment_id=experiment_id, correct_sample=correct_sample
    )
    sample_flight = sample_flight_repository.create(data=sample_flight_data)

    return sample_flight


def delete_sample_flight_by_id(
    *,
    sample_flight_id: int,
    sample_flight_repository: SampleFlightRepository,
) -> bool:
    """Deletes a sample flight by its id."""
    try:
        sample_flight_repository.delete(id=sample_flight_id)
        return True
    except NoResultFound:
        error_message = f"Sample flight with id {sample_flight_id} not found."
        logger.error(error_message)
        raise errors.ObjectNotFoundError(error_message)


def get_all_observations_for_experiment(
    *,
    experiment_id: int,
    sample_flight_repository: SampleFlightRepository,
    sample_flight_token_repository: SampleFlightRepository,
    response_repository: SampleFlightRepository,
) -> list[schemas.SampleFlightOutSchema]:
    """Gets all sample flights for a given experiment."""
    try:
        sample_flights = sample_flight_repository.filter(experiment_id=experiment_id)  # pyright: ignore[reportCallIssue]
        observations: list[schemas.ObservationSchema] = []
        for sample_flight in sample_flights:
            sample_flight_tokens = sample_flight_token_repository.filter(
                sample_flight_id=sample_flight.id  # pyright: ignore[reportCallIssue]
            )
            for token in sample_flight_tokens:
                responses = response_repository.filter(sample_flight_token_id=token.id)  # pyright: ignore[reportCallIssue]
                observations.extend(responses)
        return sample_flights
    except NoResultFound:
        error_message = (
            f"No sample flights found for experiment with id {experiment_id}."
        )
        logger.error(error_message)
        raise errors.ObjectNotFoundError(error_message)
