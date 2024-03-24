from datetime import date
from datetime import datetime
from typing import Self
from typing import Type

from scipy import stats
from sqlalchemy import DateTime
from sqlalchemy import Enum
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from triangler_fastapi import token_utils
from triangler_fastapi.constants import ExperienceLevels
from triangler_fastapi.constants import SampleNames
from triangler_fastapi.persistence import Base


class TrianglerBaseModel(Base):
    """A base for all models."""

    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, onupdate=datetime.utcnow
    )


class Experiment(TrianglerBaseModel):
    __tablename__ = "experiment"

    name: Mapped[str] = mapped_column(index=True)
    description: Mapped[str] = mapped_column()
    start_on: Mapped[date] = mapped_column()
    end_on: Mapped[date] = mapped_column()
    observations: Mapped[list["Observation"]] = relationship(
        back_populates="experiment"
    )
    observation_responses: Mapped[list["ObservationResponse"]] = relationship(
        back_populates="experiment"
    )

    def __repr__(self: Self) -> str:
        return f"{self.__tablename__}(" f"id={self.id!r}, " f"name={self.name!r}, " ")"

    @property
    def sample_size(self: Self) -> int:
        return len(self.observations)

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
        observed_correct = len([1 for x in self.observation_responses if x.is_correct])
        observed_incorrect = n_samples - observed_correct

        correct_x2 = (abs(observed_correct - expected_correct) ** 2) / expected_correct
        incorrect_x2 = (
            abs(observed_incorrect - expected_incorrect) ** 2
        ) / expected_incorrect

        x2 = correct_x2 + incorrect_x2

        return float(1 - stats.chi2.cdf(x2, 1))


class Observation(TrianglerBaseModel):
    __tablename__ = "observation"

    correct_sample: Mapped[Enum] = mapped_column(Enum(SampleNames))
    experiment_id: Mapped[int] = mapped_column(ForeignKey("experiment.id"))
    experiment: Mapped["Experiment"] = relationship(back_populates="observations")
    response: Mapped["ObservationResponse"] = relationship(back_populates="observation")
    token: Mapped["ObservationToken"] = relationship(back_populates="observation")

    def __repr__(self: Self) -> str:
        return (
            f"{self.__tablename__}("
            f"id={self.id!r}, "
            f"correct_sample={self.correct_sample!r}, "
            ")"
        )


class ObservationResponse(TrianglerBaseModel):
    __tablename__ = "observation_response"

    experiment_id: Mapped[int] = mapped_column(ForeignKey("experiment.id"))
    experiment: Mapped["Experiment"] = relationship(
        back_populates="observation_responses"
    )
    experience_level: Mapped[Enum] = mapped_column(Enum(ExperienceLevels))
    chosen_sample: Mapped[Enum] = mapped_column(Enum(SampleNames))
    responsed_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    observation_id: Mapped[int] = mapped_column(ForeignKey("observation.id"))
    observation: Mapped["Observation"] = relationship(back_populates="response")

    @property
    def is_correct(self: Self) -> bool:
        if self.observation and self.observation.correct_sample == self.chosen_sample:
            return True
        return False


class ObservationToken(TrianglerBaseModel):
    __tablename__ = "observation_token"

    token: Mapped[str] = mapped_column(String(length=32), unique=True, index=True)
    expiry_date: Mapped[datetime] = mapped_column(DateTime)
    observation_id: Mapped[int] = mapped_column(ForeignKey("observation.id"))
    observation: Mapped["Observation"] = relationship(back_populates="token")

    @classmethod
    def create_token_for_observation(cls: Type[Self], observation_id: int) -> Self:
        observation = Observation.objects.get(id=observation_id)
        token = token_utils.generate_unique_token()
        expiry_date = token_utils.calculate_expiry_date()
        return cls.objects.create(
            token=token,
            expiry_date=expiry_date,
            observation=observation,
        )

    @classmethod
    def get_observation_for_token(cls: Type[Self], token: str) -> Observation:
        return cls.objects.get(token=token).observation

    def refresh_token(self: Self) -> Self:
        self.expiry_date = token_utils.calculate_expiry_date()
        self.save()
        return self
