from datetime import date
from datetime import datetime
from typing import ClassVar
from typing import Self

from sqlalchemy import DateTime
from sqlalchemy import Enum
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from triangler_fastapi.constants import ExperienceLevels
from triangler_fastapi.constants import SampleNames
from triangler_fastapi.data.persistence import Base
from triangler_fastapi.domain import datetime_utils


class TrianglerBaseModel(Base):  # pyright: ignore[reportUntypedBaseClass, reportGeneralTypeIssues]
    """A base for all models."""

    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime_utils.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime_utils.utcnow, onupdate=datetime_utils.utcnow
    )


class Experiment(TrianglerBaseModel):
    __tablename__ = "experiment"
    __mapper_args__: ClassVar = {"eager_defaults": True}

    name: Mapped[str] = mapped_column(index=True)
    description: Mapped[str] = mapped_column()
    start_on: Mapped[date] = mapped_column()
    end_on: Mapped[date] = mapped_column()
    sample_flights: Mapped[list["SampleFlight"]] = relationship(
        back_populates="experiment", lazy="raise"
    )

    def __repr__(self: Self) -> str:
        return f"{self.__tablename__}(id={self.id!r}, name={self.name!r})"


class SampleFlight(TrianglerBaseModel):
    __tablename__ = "sample_flight"
    __mapper_args__: ClassVar = {"eager_defaults": True}

    correct_sample: Mapped[Enum] = mapped_column(Enum(SampleNames))
    experiment_id: Mapped[int] = mapped_column(ForeignKey("experiment.id"))
    experiment: Mapped["Experiment"] = relationship(
        back_populates="sample_flights", lazy="raise"
    )
    response: Mapped["Response"] = relationship(
        back_populates="sample_flight", lazy="raise"
    )
    token: Mapped["SampleFlightToken"] = relationship(
        back_populates="sample_flight", lazy="raise"
    )

    def __repr__(self: Self) -> str:
        return (
            f"{self.__tablename__}("
            f"id={self.id!r}, "
            f"correct_sample={self.correct_sample!r}, "
            ")"
        )


class Response(TrianglerBaseModel):
    __tablename__ = "response"
    __mapper_args__: ClassVar = {"eager_defaults": True}

    experience_level: Mapped[Enum] = mapped_column(Enum(ExperienceLevels))
    chosen_sample: Mapped[Enum] = mapped_column(Enum(SampleNames))
    responded_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime_utils.utcnow, onupdate=datetime_utils.utcnow
    )
    sample_flight_id: Mapped[int] = mapped_column(ForeignKey("sample_flight.id"))
    sample_flight: Mapped["SampleFlight"] = relationship(
        back_populates="response", lazy="raise"
    )
    token: Mapped["SampleFlightToken"] = relationship(
        back_populates="response", lazy="raise"
    )


class SampleFlightToken(TrianglerBaseModel):
    __tablename__ = "sample_flight_token"
    __mapper_args__: ClassVar = {"eager_defaults": True}

    token: Mapped[str] = mapped_column(String(length=32), unique=True, index=True)
    expiry_date: Mapped[datetime] = mapped_column(DateTime)
    response_id: Mapped[int] = mapped_column(ForeignKey("response.id"))
    response: Mapped["Response"] = relationship(back_populates="token", lazy="raise")
    sample_flight_id: Mapped[int] = mapped_column(ForeignKey("sample_flight.id"))
    sample_flight: Mapped["SampleFlight"] = relationship(
        back_populates="token", lazy="raise"
    )
