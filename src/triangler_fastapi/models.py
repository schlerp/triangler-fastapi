from datetime import date
from datetime import datetime
from typing import Self
from typing import Type

from sqlalchemy import DateTime
from sqlalchemy import Enum
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from triangler_fastapi import datetime_utils
from triangler_fastapi import token_utils
from triangler_fastapi.constants import ExperienceLevels
from triangler_fastapi.constants import SampleNames
from triangler_fastapi.persistence import Base


class TrianglerBaseModel(Base):
    """A base for all models."""

    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime_utils.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime_utils.utcnow, onupdate=datetime_utils.utcnow
    )


class Experiment(TrianglerBaseModel):
    __tablename__ = "experiment"

    name: Mapped[str] = mapped_column(index=True)
    description: Mapped[str] = mapped_column()
    start_on: Mapped[date] = mapped_column()
    end_on: Mapped[date] = mapped_column()
    sample_flights: Mapped[list["SampleFlight"]] = relationship(
        back_populates="experiment", lazy=False
    )

    def __repr__(self: Self) -> str:
        return f"{self.__tablename__}(" f"id={self.id!r}, " f"name={self.name!r}, " ")"


class SampleFlight(TrianglerBaseModel):
    __tablename__ = "sample_flight"

    correct_sample: Mapped[Enum] = mapped_column(Enum(SampleNames))
    experiment_id: Mapped[int] = mapped_column(ForeignKey("experiment.id"))
    experiment: Mapped["Experiment"] = relationship(
        back_populates="sample_flights", lazy=False
    )
    observation: Mapped["Observation"] = relationship(
        back_populates="sample_flight", lazy=False
    )
    token: Mapped["SampleFlightToken"] = relationship(
        back_populates="sample_flight", lazy=False
    )

    def __repr__(self: Self) -> str:
        return (
            f"{self.__tablename__}("
            f"id={self.id!r}, "
            f"correct_sample={self.correct_sample!r}, "
            ")"
        )


class Observation(TrianglerBaseModel):
    __tablename__ = "observation"

    experience_level: Mapped[Enum] = mapped_column(Enum(ExperienceLevels))
    chosen_sample: Mapped[Enum] = mapped_column(Enum(SampleNames))
    responded_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime_utils.utcnow, onupdate=datetime_utils.utcnow
    )
    sample_flight_id: Mapped[int] = mapped_column(ForeignKey("sample_flight.id"))
    sample_flight: Mapped["SampleFlight"] = relationship(
        back_populates="observation", lazy=False
    )
    token: Mapped["SampleFlightToken"] = relationship(
        back_populates="observation", lazy=False
    )

    @property
    def is_correct(self: Self) -> bool:
        if self.observation and self.observation.correct_sample == self.chosen_sample:
            return True
        return False


class SampleFlightToken(TrianglerBaseModel):
    __tablename__ = "sample_flight_token"

    token: Mapped[str] = mapped_column(String(length=32), unique=True, index=True)
    expiry_date: Mapped[datetime] = mapped_column(DateTime)
    observation_id: Mapped[int] = mapped_column(ForeignKey("observation.id"))
    observation: Mapped["Observation"] = relationship(
        back_populates="token", lazy=False
    )
    sample_flight_id: Mapped[int] = mapped_column(ForeignKey("sample_flight.id"))
    sample_flight: Mapped["SampleFlight"] = relationship(
        back_populates="token", lazy=False
    )

    @classmethod
    def create_token_for_observation(cls: Type[Self], observation_id: int) -> Self:
        observation = SampleFlight.objects.get(id=observation_id)
        token = token_utils.generate_unique_token()
        expiry_date = token_utils.calculate_expiry_date()
        return cls.objects.create(
            token=token,
            expiry_date=expiry_date,
            observation=observation,
        )

    @classmethod
    def get_observation_for_token(cls: Type[Self], token: str) -> SampleFlight:
        return cls.objects.get(token=token).observation

    def refresh_token(self: Self) -> Self:
        self.expiry_date = token_utils.calculate_expiry_date()
        self.save()
        return self
