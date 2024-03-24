from fastapi import APIRouter
from fastapi import HTTPException

from triangler_fastapi import schemas
from triangler_fastapi import usecases

EXPERIMENT_TAG = "Experiments"

router = APIRouter(
    prefix="/experiments",
    tags=["v1"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", tags=[EXPERIMENT_TAG], status_code=200)
def get_all_experiments() -> list[schemas.ExperimentOutSchema]:
    """Gets all experiments defined in this application."""
    experiment_results = usecases.get_all_experiments()
    return [schemas.ExperimentOutSchema.model_validate(x) for x in experiment_results]


@router.get("/{experiment_id}", tags=[EXPERIMENT_TAG], status_code=200)
def get_experiment_by_id(experiment_id: int) -> schemas.ExperimentOutSchema:
    """Get a specific experiemnt by its experiment ID."""
    experiment = usecases.get_experiment_by_id(id=experiment_id)
    if experiment is None:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return schemas.ExperimentOutSchema.model_validate(experiment)


@router.post("/", tags=[EXPERIMENT_TAG], status_code=201)
def create_experiment(
    payload: schemas.ExperimentInSchema,
) -> schemas.ExperimentOutSchema:
    """Creates a new experiment with the supplied payload, returns the experiment id."""
    experiment = usecases.create_experiment(
        name=payload.name,
        description=payload.description,
        start_on=payload.start_on,
        end_on=payload.end_on,
    )
    return schemas.ExperimentOutSchema.model_validate(experiment)


@router.put("/{experiment_id}", tags=[EXPERIMENT_TAG], status_code=200)
def update_experiment(
    experiment_id: int, payload: schemas.ExperimentInSchema
) -> schemas.ActionSuccessful | schemas.ActionFailed:
    """Updates the experiment with `experiment_id`, using supplied payload"""
    # TODO: should we return the updated experiment?
    try:
        _ = usecases.update_experiment(
            experiment_id=experiment_id,
            name=payload.name,
            description=payload.description,
            start_on=payload.start_on,
            end_on=payload.end_on,
        )
        return schemas.ActionSuccessful(
            message="Experiment updated successfully.", details={"id": experiment_id}
        )
    except ValueError as e:
        return schemas.ActionFailed(message=str(e))
    except Exception as e:
        return schemas.ActionFailed(
            message="An error occurred.",
            details={"error": str(e)},  # TODO: remove this in production
        )


@router.delete("/{experiment_id}", tags=[EXPERIMENT_TAG], status_code=200)
def delete_experiment(
    experiment_id: int,
) -> schemas.ActionSuccessful | schemas.ActionFailed:
    """Deletes the experiment with a matching id."""
    try:
        usecases.delete_experiment(
            experiment_id=experiment_id,
        )
        return schemas.ActionSuccessful(
            message="Experiment was deleted.", details={"id": experiment_id}
        )
    except ValueError as e:
        return schemas.ActionFailed(message=str(e))
    except Exception as e:
        return schemas.ActionFailed(
            message="An error occurred.",
            details={"error": str(e)},  # TODO: remove this in production
        )
