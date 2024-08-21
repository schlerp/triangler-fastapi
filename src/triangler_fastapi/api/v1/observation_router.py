from enum import Enum

from fastapi import APIRouter

# from fastapi import HTTPException
# from loguru import logger

# from triangler_fastapi import schemas
# from triangler_fastapi import usecases

ROUTER_TAGS: list[str | Enum] = ["Observations", "v1"]
ROUTER_PATH = "/observations"

router = APIRouter(
    prefix=ROUTER_PATH,
    tags=ROUTER_TAGS,
    responses={404: {"description": "Not found"}},
)


# @router.get("/", status_code=200)
# def get_all_observations() -> list[schemas.ExperimentOutSchema]:
#    """Gets all observations defined in this application."""
#    experiment_results = usecases.get_all_experiments()
#    return [schemas.ExperimentOutSchema.model_validate(x) for x in experiment_results]
#
#
# @router.get("/experiemnt/{experiment_id}", status_code=200)
# def get_all_observations_for_experiment(
#    experiment_id: int,
# ) -> list[schemas.ObservationOutSchema]:
#    """Gets all observations for a given experiment."""
#    experiment_results = usecases.get_all_experiments()
#    return [schemas.ObservationOutSchema.model_validate(x) for x in experiment_results]
#
#
# @router.get("/{observation_id}", status_code=200)
# def get_observation_by_id(observation_id: int) -> schemas.ExperimentOutSchema:
#    """Get a specific experiemnt by its observation ID."""
#    observation = usecases.get_experiment_by_id(id=observation_id)
#    if observation is None:
#        logger.error(f"Experiment with id {observation_id} not found.")
#        raise HTTPException(status_code=404, detail="Observation not found")
#    return schemas.ExperimentOutSchema.model_validate(observation)
#
#
# @router.post("/", status_code=201)
# def create_experiment(
#    payload: schemas.ExperimentInSchema,
# ) -> schemas.ExperimentOutSchema:
#    """Creates a new experiment with the supplied payload, returns the experiment id."""
#    experiment = usecases.create_experiment(
#        name=payload.name,
#        description=payload.description,
#        start_on=payload.start_on,
#        end_on=payload.end_on,
#    )
#    return schemas.ExperimentOutSchema.model_validate(experiment)
#
#
# @router.put("/{experiment_id}", status_code=200)
# def update_experiment(
#    experiment_id: int, payload: schemas.ExperimentInSchema
# ) -> schemas.ActionOutcome | schemas.ActionOutcome:
#    """Updates the experiment with `experiment_id`, using supplied payload"""
#    # TODO: should we return the updated experiment?
#    try:
#        _ = usecases.update_experiment(
#            experiment_id=experiment_id,
#            name=payload.name,
#            description=payload.description,
#            start_on=payload.start_on,
#            end_on=payload.end_on,
#        )
#        return schemas.ActionOutcome(
#            success=True,
#            message="Experiment updated successfully.",
#            details={"id": experiment_id},
#        )
#    except ValueError as e:
#        logger.error(f"Error updating experiment: {e}")
#        return schemas.ActionOutcome(success=False, message=str(e))
#    except Exception as e:
#        logger.error(f"Error updating experiment: {e}")
#        return schemas.ActionOutcome(
#            success=False,
#            message="An error occurred.",
#            details={"error": str(e)},  # TODO: remove this in production
#        )
#
#
# @router.delete("/{experiment_id}", status_code=200)
# def delete_experiment(
#    experiment_id: int,
# ) -> schemas.ActionOutcome | schemas.ActionOutcome:
#    """Deletes the experiment with a matching id."""
#    try:
#        usecases.delete_experiment(
#            experiment_id=experiment_id,
#        )
#        return schemas.ActionOutcome(
#            success=True,
#            message="Experiment was deleted.",
#            details={"id": experiment_id},
#        )
#    except ValueError as e:
#        logger.error(f"Error deleting experiment: {e}")
#        return schemas.ActionOutcome(success=False, message=str(e))
#    except Exception as e:
#        logger.error(f"Error deleting experiment: {e}")
#        return schemas.ActionOutcome(
#            success=False,
#            message="An error occurred.",
#            details={"error": str(e)},  # TODO: remove this in production
#        )
