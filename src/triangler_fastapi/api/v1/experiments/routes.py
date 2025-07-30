from enum import Enum

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from triangler_fastapi.data import models
from triangler_fastapi.domain import repositories
from triangler_fastapi.domain import schemas
from triangler_fastapi.exceptions import errors
from triangler_fastapi.services import experiment_service

from . import depends

ROUTER_TAGS: list[str | Enum] = ["Experiments", "v1"]
ROUTER_PATH = "/experiments"

router = APIRouter(
    prefix=ROUTER_PATH,
    tags=ROUTER_TAGS,
    responses={404: {"description": "Not found"}},
)


@router.get("/", status_code=200)
def get_all_experiments(
    repository: repositories.ExperimentRepository = Depends(
        depends.get_repository(models.Experiment)
    ),
) -> list[schemas.ExperimentOutSchema]:
    """Gets all experiments defined in this application."""
    experiment_results = experiment_service.get_all_experiments(repository=repository)
    return experiment_results


@router.get("/{experiment_id}", status_code=200)
def get_experiment_by_id(
    experiment_id: int,
    repository: repositories.ExperimentRepository = Depends(
        depends.get_repository(models.Experiment)
    ),
) -> schemas.ExperimentOutSchema:
    """Get a specific experiemnt by its experiment ID."""
    try:
        experiment = experiment_service.get_experiment_by_id(
            id=experiment_id, repository=repository
        )
    except errors.ObjectNotFoundError as e:
        raise HTTPException(status_code=404, detail="Experiment not found") from e
    return experiment


@router.post("/", status_code=201)
def create_experiment(
    payload: schemas.ExperimentInSchema,
    repository: repositories.ExperimentRepository = Depends(
        depends.get_repository(models.Experiment)
    ),
) -> schemas.ExperimentOutSchema:
    """Creates a new experiment with the supplied payload, returns the experiment id."""
    experiment = experiment_service.create_experiment(
        data=payload, repository=repository
    )
    return schemas.ExperimentOutSchema.model_validate(experiment)


@router.put("/{experiment_id}", status_code=200)
def update_experiment(
    experiment_id: int,
    payload: schemas.ExperimentUpdateSchema,
    repository: repositories.ExperimentRepository = Depends(
        depends.get_repository(models.Experiment)
    ),
) -> schemas.ExperimentOutSchema:
    """Updates the experiment with `experiment_id`, using supplied payload"""
    try:
        updated_data = experiment_service.update_experiment(
            id=experiment_id, update_data=payload, repository=repository
        )
    except errors.ObjectNotFoundError as e:
        raise HTTPException(status_code=404, detail="Experiment not found") from e
    return updated_data


@router.delete("/{experiment_id}", status_code=200)
def delete_experiment(
    experiment_id: int,
    repository: repositories.ExperimentRepository = Depends(
        depends.get_repository(models.Experiment)
    ),
) -> schemas.ActionOutcome:
    """Deletes the experiment with a matching id."""
    try:
        experiment_service.delete_experiment(id=experiment_id, repository=repository)
    except errors.ObjectNotFoundError:
        raise HTTPException(status_code=404, detail="Experiment not found")

    return schemas.ActionOutcome(
        success=True,
        message="Experiment found, proceeding to delete.",
        details={"id": experiment_id},
    )
