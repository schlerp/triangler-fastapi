from datetime import datetime
from datetime import timedelta
from datetime import timezone
from typing import TypeAlias

from jose import jwt
from sqlalchemy import select

from triangler_fastapi import persistence
from triangler_fastapi.auth import constants
from triangler_fastapi.auth import exceptions
from triangler_fastapi.auth import models
from triangler_fastapi.auth import rbac
from triangler_fastapi.auth import schemas


def create_user_from_schema(user: schemas.UserCreate) -> schemas.User:
    """Create a user model in the database"""
    with persistence.SessionLocal() as session:
        if session.query(
            select(models.User).filter(models.User.username == user.username).exists()
        ).scalar():
            raise exceptions.UserAlreadyExistsError(username=user.username)

        user_model = models.User(
            username=user.username,
            email=user.email,
            hashed_password=user.hashed_password,
            salt=user.salt,
        )
        session.add(user_model)
        session.commit()
        session.refresh(user_model)
        user_schema = schemas.User.model_validate(user_model)
    return user_schema


def get_user(username: str) -> schemas.User | None:
    """Gets an experiment by its id."""
    with persistence.SessionLocal() as session:
        result = session.scalars(
            select(models.User).where(models.User.username == username).order_by("id")
        ).first()
        if not result:
            return None
        result_schema = schemas.User.model_validate(result)
    return result_schema


def disable_user(username: str) -> schemas.User:
    """Marks a user as disabled by its username."""
    with persistence.SessionLocal() as session:
        result = session.scalars(
            select(models.User).where(models.User.username == username).order_by("id")
        ).first()

        if not result:
            raise exceptions.UserNotExistsError(username=username)

        result.disabled = True
        session.add(result)
        session.commit()
        result_schema = schemas.User.model_validate(result)
    return result_schema


def authenticate_user(login_data: schemas.LoginPayload) -> schemas.User:
    with persistence.SessionLocal() as session:
        # get the user with that username
        user_model = session.scalars(
            select(models.User)
            .where(models.User.username == login_data.username)
            .order_by(models.User.username)
        ).first()

        if not user_model:
            raise exceptions.AuthenticationFailedError(constants.USER_NOT_FOUND_DETAIL)

        # ensure the user is active
        if user_model.disabled:
            raise exceptions.AuthenticationFailedError(constants.USER_DISABLED_DETAIL)

        user = schemas.User.model_validate(user_model)

    # validate that the passwords match
    if not user.validate_password(login_data.password):
        raise exceptions.AuthenticationFailedError(
            constants.USER_VALIDATION_FAILED_DETAIL
        )

    return user


JWToken: TypeAlias = str


def create_access_token(user: schemas.User) -> JWToken:
    access_token_expires = timedelta(minutes=constants.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"sub": user.username, "scopes": [x for x in user.roles]}
    expire = datetime.now(timezone.utc) + access_token_expires
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, constants.JWT_SECRET_KEY, algorithm=constants.JWT_ALGORITHM
    )
    return encoded_jwt


def upgrade_user_to_admin(user: schemas.UserCreate) -> schemas.User:
    if rbac.ADMIN_ROLE in user.roles:
        raise ValueError("User is already an admin")
    user.roles.append(rbac.ADMIN_ROLE)
    return create_user_from_schema(user)
