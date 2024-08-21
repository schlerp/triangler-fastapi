import datetime
from typing import Self

import pytest

from triangler_fastapi import schemas


class TestJustIdSchema:
    def test_create_instance(self: Self) -> None:
        """Test that we can create an instance of JustIdSchema."""
        schema = schemas.JustIdSchema(id=1)
        assert schema.id == 1

    def test_create_invalid_instance(self: Self) -> None:
        """Test that we cannot create an invalid instance of JustIdSchema."""
        with pytest.raises(ValueError):
            schemas.JustIdSchema(id=-1)


class TestActionOutcomeSchema:
    def test_create_instance(self: Self) -> None:
        """Test that we can create an instance of ActionOutcome."""
        schema = schemas.ActionOutcome(success=True, message="test")
        assert schema.success is True
        assert schema.message == "test"
        assert schema.details is None

    def test_create_instance_with_details(self: Self) -> None:
        """Test that we can create an instance of ActionOutcome with details."""
        schema = schemas.ActionOutcome(
            success=True, message="test", details={"test": "test"}
        )
        assert schema.success is True
        assert schema.message == "test"
        assert schema.details == {"test": "test"}

    def test_create_invalid_instance(self: Self) -> None:
        """Test that we cannot create an invalid instance of ActionOutcome."""
        with pytest.raises(ValueError):
            schemas.ActionOutcome(success=False, message="")


class TestTrianglerOutBaseSchema:
    def test_create_instance(self: Self) -> None:
        """Test that we can create an instance of TrianglerOutBaseSchema."""
        created_at = datetime.datetime(
            year=2000, month=1, day=1, hour=0, minute=0, second=0
        )
        updated_at = datetime.datetime(
            year=2000, month=1, day=1, hour=0, minute=0, second=0
        )
        schema = schemas.TrianglerOutBaseSchema(
            id=1,
            created_at=created_at,
            updated_at=updated_at,
        )
        assert schema.id == 1

    def test_create_invalid_instance(self: Self) -> None:
        """Test that we cannot create an invalid instance of TrianglerOutBaseSchema."""
        with pytest.raises(ValueError):
            created_at = datetime.datetime(
                year=2001, month=1, day=1, hour=0, minute=0, second=0
            )
            updated_at = datetime.datetime(
                year=2000, month=1, day=1, hour=0, minute=0, second=0
            )
            schemas.TrianglerOutBaseSchema(
                id=1,
                created_at=created_at,
                updated_at=updated_at,
            )


class TestExperimentBaseSchema:
    def test_create_instance(self: Self) -> None:
        """Test that we can create an instance of ExperimentBaseSchema."""
        start_on = datetime.date(year=2000, month=1, day=1)
        end_on = datetime.date(year=2000, month=1, day=2)
        schema = schemas.ExperimentBaseSchema(
            name="test",
            description="test",
            start_on=start_on,
            end_on=end_on,
        )
        assert schema.name == "test"

    def test_create_invalid_instance(self: Self) -> None:
        """Test that we cannot create an invalid instance of ExperimentBaseSchema."""
        with pytest.raises(ValueError):
            start_on = datetime.date(year=2000, month=1, day=2)
            end_on = datetime.date(year=2000, month=1, day=1)
            schemas.ExperimentBaseSchema(
                name="test",
                description="test",
                start_on=start_on,
                end_on=end_on,
            )
