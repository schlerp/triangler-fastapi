from typing import Callable

from fastapi import Depends
from sqlalchemy.orm import Session

from triangler_fastapi.data import models
from triangler_fastapi.data import persistence
from triangler_fastapi.domain import repositories
from triangler_fastapi.domain import schemas


def get_repository(
    data_model: type[models.TrianglerBaseModel],
) -> Callable[
    [Session],
    repositories.Repository[
        models.TrianglerBaseModel,
        schemas.TrianglerBaseInSchema,
        schemas.TrianglerBaseOutSchema,
    ],
]:
    def func(  # pyright: ignore[reportUnknownParameterType]
        session: Session = Depends(persistence.get_db_session),  # pyright: ignore[reportCallInDefaultInitializer]
    ) -> repositories.Repository:  # pyright: ignore[reportMissingTypeArgument]
        if data_model is models.Experiment:
            return repositories.ExperimentRepository(
                session=session,
                data_model=models.Experiment,
                schema_in=schemas.ExperimentInSchema,
                schema_out=schemas.ExperimentOutSchema,
            )
        elif data_model is models.SampleFlight:
            return repositories.SampleFlightRepository(
                session=session,
                data_model=models.SampleFlight,
                schema_in=schemas.SampleFlightInSchema,
                schema_out=schemas.SampleFlightOutSchema,
            )
        elif data_model is models.Response:
            return repositories.ResponseRepository(
                session=session,
                data_model=models.Response,
                schema_in=schemas.ResponseInSchema,
                schema_out=schemas.ResponseOutSchema,
            )
        elif data_model is models.SampleFlightToken:
            return repositories.SampleFlightTokenRepository(
                session=session,
                data_model=models.SampleFlightToken,
                schema_in=schemas.SampleFlightTokenInSchema,
                schema_out=schemas.SampleFlightTokenOutSchema,
            )

        raise ValueError(f"Unknown data model: {data_model}")

    return func  # pyright: ignore[reportUnknownVariableType]
