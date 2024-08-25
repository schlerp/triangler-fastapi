from datetime import date
from datetime import datetime
from typing import Annotated
from typing import Any
from typing import Optional
from typing import Self

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field
from pydantic import model_validator
from scipy import stats

from triangler_fastapi import token_utils

PositiveInt = Annotated[int, Field(ge=0)]


class TrianglerBaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class TrianglerBaseInSchema(TrianglerBaseSchema): ...


class JustIdSchema(TrianglerBaseSchema):
    id: PositiveInt


class ActionOutcome(TrianglerBaseSchema):
    success: bool
    message: str
    details: Optional[dict[str, Any]] = None

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


class ExperimentOutSchema(TrianglerBaseOutSchema, ExperimentBaseSchema):
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

        # number of correct observations
        observed_correct = len([1 for x in self.sample_flights if x.is_correct])
        observed_incorrect = n_samples - observed_correct

        correct_x2 = (abs(observed_correct - expected_correct) ** 2) / expected_correct
        incorrect_x2 = (
            abs(observed_incorrect - expected_incorrect) ** 2
        ) / expected_incorrect

        x2 = correct_x2 + incorrect_x2

        return float(1 - stats.chi2.cdf(x2, 1))


class ObservationBaseSchema(TrianglerBaseSchema):
    observation_id: int
    response: str
    is_correct: bool


class ObservationInSchema(ObservationBaseSchema, TrianglerBaseInSchema): ...


class ObservationOutSchema(TrianglerBaseOutSchema, ObservationBaseSchema): ...


class SampleFlightBaseSchema(TrianglerBaseSchema):
    experiment_id: int
    correct_sample: str
    observation: ObservationBaseSchema | None = None

    @property
    def is_correct(self: Self) -> bool:
        if self.observation is None:
            return False
        return self.correct_sample == self.observation.response


class SampleFlightInSchema(SampleFlightBaseSchema, TrianglerBaseInSchema): ...


class SampleFlightOutSchema(TrianglerBaseOutSchema, SampleFlightBaseSchema): ...


class SampleFlightTokenBaseSchema(TrianglerBaseSchema):
    token: str
    expiry_date: datetime
    observation_id: int

    @property
    def qr_code_svg(self: Self) -> str:
        return token_utils.generate_qr_code_svg(self.token)


class SampleFlightTokenInSchema(SampleFlightTokenBaseSchema, TrianglerBaseInSchema): ...


class SampleFlightTokenOutSchema(
    TrianglerBaseOutSchema, SampleFlightTokenBaseSchema
): ...
