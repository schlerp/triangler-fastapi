from collections.abc import Sequence
from datetime import datetime

from sqlalchemy import select

from triangler_fastapi import models
from triangler_fastapi import persistence
from triangler_fastapi import schemas


def get_all_experiments() -> Sequence[schemas.ExperimentOutSchema]:
    """Gets all experiemnts from the database."""
    with persistence.SessionLocal() as session:
        results = [
            schemas.ExperimentOutSchema.model_validate(x)
            for x in session.scalars(
                select(models.Experiment).order_by(models.Experiment.name)
            ).all()
        ]
        session.commit()
    return results


def get_experiment_by_id(id: int) -> schemas.ExperimentOutSchema | None:
    """Gets an experiment by its id."""
    with persistence.SessionLocal() as session:
        result = session.scalars(
            select(models.Experiment)
            .where(models.Experiment.id == id)
            .order_by(models.Experiment.name)
        ).first()
        if not result:
            return None
        result_schema = schemas.ExperimentOutSchema.model_validate(result)
    return result_schema


def create_experiment(
    name: str,
    description: str,
    start_on: datetime,
    end_on: datetime,
) -> schemas.ExperimentOutSchema:
    with persistence.SessionLocal() as session:
        new_experiment = models.Experiment(
            name=name, description=description, start_on=start_on, end_on=end_on
        )
        session.add(new_experiment)
        session.commit()
        result_schema = schemas.ExperimentOutSchema.model_validate(new_experiment)
    return result_schema


def update_experiment(
    experiment_id: int,
    name: str | None = None,
    description: str | None = None,
    start_on: datetime | None = None,
    end_on: datetime | None = None,
) -> schemas.ExperimentOutSchema:
    with persistence.SessionLocal() as session:
        experiment = session.scalars(
            select(models.Experiment)
            .where(models.Experiment.id == experiment_id)
            .order_by(models.Experiment.name)
        ).first()
        if experiment is None:
            raise ValueError(f"Experiment with id {experiment_id} not found.")
        if name is not None:
            experiment.name = name
        if description is not None:
            experiment.description = description
        if start_on is not None:
            experiment.start_on = start_on
        if end_on is not None:
            experiment.end_on = end_on
        session.commit()
        result_schema = schemas.ExperimentOutSchema.model_validate(experiment)
    return result_schema


def delete_experiment(experiment_id: int) -> None:
    """Deletes an experiment by its id."""
    with persistence.SessionLocal() as session:
        experiment = session.scalars(
            select(models.Experiment)
            .where(models.Experiment.id == experiment_id)
            .order_by(models.Experiment.name)
        ).first()
        if experiment is None:
            raise ValueError(f"Experiment with id {experiment_id} not found.")
        session.delete(experiment)
        session.commit()
    return None
