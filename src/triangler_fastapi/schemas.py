from datetime import datetime
from typing import Any
from typing import Optional
from typing import Self

from pydantic import BaseModel
from pydantic import ConfigDict

from triangler_fastapi import token_utils


class TrianglerBaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class JustIdSchema(TrianglerBaseSchema):
    id: int


class ActionSuccessful(TrianglerBaseSchema):
    message: str
    details: Optional[dict[str, Any]] = None


class ActionFailed(TrianglerBaseSchema):
    message: str
    details: Optional[dict[str, Any]] = None


class TrianglerOutBaseSchema(TrianglerBaseSchema):
    id: int
    created_at: datetime
    updated_at: datetime


class ExperimentBaseSchema(TrianglerBaseSchema):
    name: str
    description: str
    start_on: datetime
    end_on: datetime


class ExperimentInSchema(ExperimentBaseSchema):
    ...


class ExperimentOutSchema(TrianglerOutBaseSchema, ExperimentBaseSchema):
    sample_size: int
    p_value: float


class ObservationBaseSchema(TrianglerBaseSchema):
    experiment_id: int
    correct_sample: str


class ObservationInSchema(ObservationBaseSchema):
    ...


class ObservationOutSchema(TrianglerOutBaseSchema, ObservationBaseSchema):
    ...


class ObservationResponseBaseSchema(TrianglerBaseSchema):
    observation_id: int
    response: str
    is_correct: bool
    created_at: datetime
    updated_at: datetime


class ObservationResponseInSchema(ObservationResponseBaseSchema):
    ...


class ObservationResponseOutSchema(
    TrianglerOutBaseSchema, ObservationResponseBaseSchema
):
    ...


class ObservationTokenBaseSchema(TrianglerBaseSchema):
    token: str
    expiry_date: datetime
    observation_id: int

    @property
    def qr_code_svg(self: Self) -> str:
        return token_utils.generate_qr_code_svg(self.token)


class ObservationTokenInSchema(ObservationTokenBaseSchema):
    ...


class ObservationTokenOutSchema(TrianglerOutBaseSchema, ObservationTokenBaseSchema):
    ...
