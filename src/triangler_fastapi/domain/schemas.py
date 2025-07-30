import random
from datetime import date
from datetime import datetime
from typing import Annotated
from typing import Any
from typing import Literal
from typing import Self

import pytz as tz
from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field
from pydantic import model_validator
from scipy import stats

from triangler_fastapi.domain import token_utils

PositiveInt = Annotated[int, Field(ge=0)]


class TrianglerBaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class TrianglerBaseInSchema(TrianglerBaseSchema): ...


class JustIdSchema(TrianglerBaseSchema):
    id: PositiveInt


class ActionOutcome(TrianglerBaseSchema):
    success: bool
    message: str
    details: dict[str, Any] | None = None

    @model_validator(mode="after")
    def ensure_message_if_not_successful(self: Self) -> Self:
        if not self.success and not self.message:
            raise ValueError("When success is False, a message must be provided.")
        return self


class TrianglerBaseOutSchema(TrianglerBaseSchema):
    id: PositiveInt
    created_at: datetime
    updated_at: datetime

    @model_validator(mode="after")
    def ensure_valid_updated_at(self: Self) -> Self:
        if self.updated_at.tzinfo is None:
            self.updated_at = tz.utc.localize(self.updated_at)
        if self.created_at.tzinfo is None:
            self.created_at = tz.utc.localize(self.created_at)
        if self.created_at > self.updated_at:
            raise ValueError(
                "Update date must be greater than or equal to create date."
            )
        return self


class ExperimentBaseSchema(TrianglerBaseSchema):
    name: str
    description: str
    start_on: date
    end_on: date

    @model_validator(mode="after")
    def ensure_valid_range(self: Self) -> Self:
        if self.start_on > self.end_on:
            raise ValueError("Start date must be before or equal to end date.")
        return self


class ExperimentInSchema(ExperimentBaseSchema, TrianglerBaseInSchema): ...


class ExperimentUpdateSchema(ExperimentBaseSchema, TrianglerBaseInSchema):
    name: str | None = None  # pyright: ignore[reportIncompatibleVariableOverride]
    description: str | None = None  # pyright: ignore[reportIncompatibleVariableOverride]
    start_on: date | None = None  # pyright: ignore[reportIncompatibleVariableOverride]
    end_on: date | None = None  # pyright: ignore[reportIncompatibleVariableOverride]


class ExperimentOutSchema(TrianglerBaseOutSchema, ExperimentBaseSchema): ...


class ExperimentEnrichedSchema(TrianglerBaseOutSchema, ExperimentBaseSchema):
    sample_flights: list["SampleFlightOutSchema"]

    @property
    def sample_size(self: Self) -> int:
        return len(self.sample_flights)

    @property
    def p_value(self: Self) -> float:
        n_samples = float(self.sample_size)
        if n_samples < 1:
            return 1.0
        # expected 1/3 of the time to be correct
        expected_correct = n_samples / 3
        # expected 2/3 of the time to be incorrect
        expected_incorrect = expected_correct * 2

        # number of correct responses
        observed_correct = len([1 for x in self.sample_flights if x.is_correct])
        observed_incorrect = n_samples - observed_correct

        correct_x2 = (abs(observed_correct - expected_correct) ** 2) / expected_correct
        incorrect_x2 = (
            abs(observed_incorrect - expected_incorrect) ** 2
        ) / expected_incorrect

        x2 = correct_x2 + incorrect_x2

        return float(1 - stats.chi2.cdf(x2, 1))


class ResponseBaseSchema(TrianglerBaseSchema):
    response_id: int
    response_choice: Literal["A", "B", "C"]
    is_correct: bool


class ResponseInSchema(ResponseBaseSchema, TrianglerBaseInSchema): ...


class ResponseOutSchema(TrianglerBaseOutSchema, ResponseBaseSchema): ...


class SampleFlightBaseSchema(TrianglerBaseSchema):
    experiment_id: int
    correct_sample: Literal["A", "B", "C"]
    response: ResponseBaseSchema | None = None

    @property
    def is_correct(self: Self) -> bool:
        if self.response is None:
            return False
        return self.correct_sample == self.response.response_choice


class SampleFlightInSchema(SampleFlightBaseSchema, TrianglerBaseInSchema):
    @classmethod
    def new(
        cls: type[Self],
        experiment_id: int,
        correct_sample: Literal["A", "B", "C"] | None = None,
        response: ResponseBaseSchema | None = None,
    ) -> Self:
        if correct_sample is None:
            correct_sample = random.choice(["A", "B", "C"])  # noqa: S311
        return cls(
            experiment_id=experiment_id,
            correct_sample=correct_sample,
            response=response,
        )


class SampleFlightOutSchema(TrianglerBaseOutSchema, SampleFlightBaseSchema): ...


class SampleFlightTokenBaseSchema(TrianglerBaseSchema):
    token: str
    expiry_date: datetime
    response_id: int

    @property
    def qr_code_svg(self: Self) -> bytes:
        return token_utils.generate_qr_code_svg(self.token)


class SampleFlightTokenInSchema(SampleFlightTokenBaseSchema, TrianglerBaseInSchema): ...


class SampleFlightTokenOutSchema(
    TrianglerBaseOutSchema, SampleFlightTokenBaseSchema
): ...


class ObservationAwaitingResponseSchema(TrianglerBaseSchema):
    sample_flight: SampleFlightOutSchema
    token: SampleFlightTokenOutSchema

    @property
    def qr_code_svg(self: Self) -> bytes:
        return self.token.qr_code_svg

    @property
    def experiment_id(self: Self) -> int:
        return self.sample_flight.experiment_id


class ObservationSchema(TrianglerBaseSchema):
    experiment_id: int
    sample_flight: SampleFlightOutSchema
    token: SampleFlightTokenOutSchema
    response: ResponseOutSchema | None = None

    @property
    def is_correct(self: Self) -> bool:
        if self.response is None:
            return False
        return self.sample_flight.correct_sample == self.response.response_choice
