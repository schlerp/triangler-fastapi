from enum import Enum

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from loguru import logger

from triangler_fastapi.data import models
from triangler_fastapi.domain import repositories
from triangler_fastapi.domain import schemas

from .. import depends

ROUTER_TAGS: list[str | Enum] = ["Observations", "v1"]
ROUTER_PATH = "/experiments"

router = APIRouter(
    prefix=ROUTER_PATH,
    tags=ROUTER_TAGS,
    responses={404: {"description": "Not found"}},
)


@router.get("/{experiment_id}/observations", status_code=200)
def get_all_observations(
    experiment_id: int,
    experiment_repository: repositories.ExperimentRepository = Depends(
        depends.get_repository(models.Experiment)
    ),
    observation_repository: repositories.ResponseRepository = Depends(
        depends.get_repository(models.Response)
    ),
) -> list[schemas.ExperimentOutSchema]:
    """Gets all observations for a given experiment."""
    experiment = experiment_repository.get_by_id(id=experiment_id)
    if experiment is None:
        logger.error(f"Experiment with id {experiment_id} not found.")
        raise HTTPException(status_code=404, detail="Experiment not found")
    return observation_repository.filter(experiment_id=experiment_id)  # pyright: ignore[reportCallIssue]


@router.post("/{experiment_id}/observations/", status_code=201)
def create_observation(
    experiment_id: int,
    payload: schemas.ResponseInSchema,
    experiment_repository: repositories.ExperimentRepository = Depends(
        depends.get_repository(models.Experiment)
    ),
    observation_repository: repositories.ResponseRepository = Depends(
        depends.get_repository(models.Response)
    ),
) -> schemas.ResponseOutSchema:
    """Creates a new observation for the specified experiment."""
    experiment = experiment_repository.get_by_id(id=experiment_id)
    if experiment is None:
        logger.error(f"Experiment with id {experiment_id} not found.")
        raise HTTPException(status_code=404, detail="Experiment not found")

    observation = observation_repository.create(data=payload)
    return schemas.ResponseOutSchema.model_validate(observation)
