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

from triangler_fastapi import token_utils

PositiveInt = Annotated[int, Field(ge=0)]


class TrianglerBaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


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


class TrianglerOutBaseSchema(TrianglerBaseSchema):
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


class ExperimentInSchema(ExperimentBaseSchema): ...


class ExperimentOutSchema(TrianglerOutBaseSchema, ExperimentBaseSchema):
    sample_size: PositiveInt
    p_value: float


class ObservationBaseSchema(TrianglerBaseSchema):
    experiment_id: int
    correct_sample: str


class ObservationInSchema(ObservationBaseSchema): ...


class ObservationOutSchema(TrianglerOutBaseSchema, ObservationBaseSchema): ...


class ObservationResponseBaseSchema(TrianglerBaseSchema):
    observation_id: int
    response: str
    is_correct: bool


class ObservationResponseInSchema(ObservationResponseBaseSchema): ...


class ObservationResponseOutSchema(
    TrianglerOutBaseSchema, ObservationResponseBaseSchema
): ...


class ObservationTokenBaseSchema(TrianglerBaseSchema):
    token: str
    expiry_date: datetime
    observation_id: int

    @property
    def qr_code_svg(self: Self) -> str:
        return token_utils.generate_qr_code_svg(self.token)


class ObservationTokenInSchema(ObservationTokenBaseSchema): ...


class ObservationTokenOutSchema(TrianglerOutBaseSchema, ObservationTokenBaseSchema): ...
