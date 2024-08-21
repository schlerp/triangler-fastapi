from datetime import date
from datetime import datetime

from pydantic import BaseModel
from pydantic import model_validator


class DateRange(BaseModel):
    start_on: date
    end_on: date

    @model_validator(mode="after")
    def ensure_valid_range(self: "DateRange") -> "DateRange":
        if self.start_on > self.end_on:
            raise ValueError("Start date must be before or equal to end date.")
        return self


class DateTimeRange(BaseModel):
    start_at: datetime
    end_at: datetime

    @model_validator(mode="after")
    def ensure_valid_range(self: "DateTimeRange") -> "DateTimeRange":
        if self.start_at > self.end_at:
            raise ValueError("Start datetime must be before or equal to end datetime.")
        return self
