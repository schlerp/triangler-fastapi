from loguru import logger
from sqlalchemy.exc import NoResultFound

from triangler_fastapi.domain import schemas
from triangler_fastapi.domain.repositories import ExperimentRepository
from triangler_fastapi.exceptions import errors


def get_all_experiments(
    *, repository: ExperimentRepository
) -> list[schemas.ExperimentOutSchema]:
    """Gets all experiemnts from the database."""
    results = repository.get_all()
    return results


def get_experiment_by_id(
    *, id: int, repository: ExperimentRepository
) -> schemas.ExperimentOutSchema:
    """Gets an experiment by its id."""
    try:
        result_schema = repository.get_by_id(id)
        return result_schema
    except NoResultFound as e:
        error_message = f"Experiment with id {id} not found."
        logger.error(error_message)
        raise errors.ObjectNotFoundError(message=error_message) from e


def create_experiment(
    *, data: schemas.ExperimentInSchema, repository: ExperimentRepository
) -> schemas.ExperimentOutSchema:
    """Creates a new experiment."""
    result_schema = repository.create(data)
    return result_schema


def update_experiment(
    *,
    id: int,
    update_data: schemas.ExperimentUpdateSchema,
    repository: ExperimentRepository,
) -> schemas.ExperimentOutSchema:
    """Updates an experiment."""
    try:
        existing_data = repository.get_by_id(id=id)
    except NoResultFound:
        error_message = f"Experiment with id {id} not found."
        logger.error(error_message)
        raise errors.ObjectNotFoundError(message=error_message)

    existing_data.name = update_data.name or existing_data.name
    existing_data.description = update_data.description or existing_data.description
    existing_data.start_on = update_data.start_on or existing_data.start_on
    existing_data.end_on = update_data.end_on or existing_data.end_on
    updated_model_schema = repository.update(data=existing_data)
    return updated_model_schema


def delete_experiment(*, id: int, repository: ExperimentRepository) -> bool:
    """Deletes an experiment by its id."""
    try:
        repository.delete(id)
        return True
    except NoResultFound as e:
        error_message = f"Experiment with id {id} not found."
        logger.error(error_message)
        raise errors.ObjectNotFoundError(message=error_message) from e
