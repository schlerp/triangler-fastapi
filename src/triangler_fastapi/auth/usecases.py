from datetime import datetime
from datetime import timedelta
from datetime import timezone

from jose import jwt
from sqlalchemy import select

from triangler_fastapi import persistence
from triangler_fastapi.auth import constants
from triangler_fastapi.auth import models
from triangler_fastapi.auth import schemas
from triangler_fastapi.exceptions import errors


def get_user(username: str) -> schemas.User | None:
    """Gets an experiment by its id."""
    with persistence.SessionLocal() as session:
        result = session.scalars(
            select(models.User)
            .where(models.User.username == username)
            .order_by(models.User)
        ).first()
        if not result:
            return None
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
            raise errors.AuthenticationFailedError("Incorrect username or password")

        # ensure the user is active
        if user_model.disabled:
            raise errors.AuthenticationFailedError("User is disabled")

        user = schemas.User.model_validate(user_model)

    # validate that the passwords match
    if not user.validate_password(login_data.password):
        raise errors.AuthenticationFailedError("Incorrect username or password")

    return user


def create_access_token(user: schemas.User) -> str:
    access_token_expires = timedelta(minutes=constants.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"sub": user.username, "scopes": [x for x in user.roles]}
    expire = datetime.now(timezone.utc) + access_token_expires
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, constants.JWT_SECRET_KEY, algorithm=constants.JWT_ALGORITHM
    )
    return encoded_jwt
