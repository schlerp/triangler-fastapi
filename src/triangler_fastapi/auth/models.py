from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from triangler_fastapi.auth.hashing import generate_salt
from triangler_fastapi.persistence import Base


class User(Base):
    """The user class for this application."""

    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    username: Mapped[str] = mapped_column(index=True, unique=True)
    email: Mapped[str] = mapped_column(index=True, unique=True)
    hashed_password: Mapped[str] = mapped_column()
    salt: Mapped[str] = mapped_column(default=generate_salt)
    disabled: Mapped[bool] = mapped_column(default=False)
    roles: Mapped[list["Roles"]] = relationship(secondary="user_roles")


class UserRoles(Base):
    """The user roles class for this application."""

    __tablename__ = "user_roles"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id"), primary_key=True, index=True
    )
    user: Mapped[User] = relationship("User")
    role_id: Mapped[int] = mapped_column(
        ForeignKey("roles.id"), primary_key=True, index=True
    )
    role: Mapped["Roles"] = relationship("Roles")
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)


class Roles(Base):
    """The role class for this application."""

    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    name: Mapped[str] = mapped_column(index=True, unique=True)
    scopes: Mapped[str] = mapped_column()
    disabled: Mapped[bool] = mapped_column(default=False)
