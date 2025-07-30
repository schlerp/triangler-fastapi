import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from triangler_fastapi.data.models import TrianglerBaseModel
from triangler_fastapi.domain.auth.hashing import generate_salt


def default_datetime() -> datetime.datetime:
    return datetime.datetime.now(datetime.UTC)


class User(TrianglerBaseModel):
    """The user class for this application."""

    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    created_at: Mapped[datetime.datetime] = mapped_column(default=default_datetime)
    username: Mapped[str] = mapped_column(index=True, unique=True)
    email: Mapped[str] = mapped_column(index=True, unique=True)
    hashed_password: Mapped[str] = mapped_column()
    salt: Mapped[str] = mapped_column(default=generate_salt)
    disabled: Mapped[bool] = mapped_column(default=False)
    roles: Mapped[set["Role"]] = relationship(
        secondary="user_roles", back_populates="users"
    )


class UserRoles(TrianglerBaseModel):
    """The user roles class for this application."""

    __tablename__ = "user_roles"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id"), primary_key=True, index=True
    )
    role_id: Mapped[int] = mapped_column(
        ForeignKey("roles.id"), primary_key=True, index=True
    )
    created_at: Mapped[datetime.datetime] = mapped_column(default=default_datetime)


class Role(TrianglerBaseModel):
    """The role class for this application."""

    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    created_at: Mapped[datetime.datetime] = mapped_column(default=default_datetime)
    name: Mapped[str] = mapped_column(index=True, unique=True)
    scopes: Mapped[str] = mapped_column()
    disabled: Mapped[bool] = mapped_column(default=False)
    users: Mapped[set["User"]] = relationship(
        secondary="user_roles", back_populates="roles"
    )
