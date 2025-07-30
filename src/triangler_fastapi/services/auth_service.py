from datetime import datetime
from datetime import timedelta
from datetime import timezone
from typing import Any
from typing import TypeAlias

from jose import jwt

from triangler_fastapi.data import auth_models
from triangler_fastapi.domain.auth import constants
from triangler_fastapi.domain.auth import rbac
from triangler_fastapi.domain.auth import schemas
from triangler_fastapi.domain.repositories import UserRepository
from triangler_fastapi.exceptions import auth_errors

JWToken: TypeAlias = str


def _get_user_by_username(username: str, repository: UserRepository) -> schemas.User:
    """Gets a user by its username."""
    users = repository.filter(auth_models.User.username == username)
    if not users:
        raise auth_errors.UserNotExistsError(username=username)
    # we are enforcing unique usernames at the database level
    user = users[0]
    user_as_schema = schemas.User.model_validate(user)
    return user_as_schema


def create_user_from_schema(
    user: schemas.UserCreate,
    repository: UserRepository,
) -> schemas.User:
    """Create a user model in the database"""
    try:
        existing_user = _get_user_by_username(user.username, repository)
    except auth_errors.UserNotExistsError:
        existing_user = None

    if existing_user:
        raise auth_errors.UserAlreadyExistsError(username=user.username)

    user_model = repository.create(user)
    user_schema = schemas.User.model_validate(user_model)
    return user_schema


def get_user(username: str, repository: UserRepository) -> schemas.User | None:
    """Gets a user by its username."""
    user_as_schema = _get_user_by_username(username, repository)
    return user_as_schema


def disable_user(username: str, repository: UserRepository) -> schemas.User:
    """Marks a user as disabled by its username."""
    user_as_schema = _get_user_by_username(username, repository)
    user_as_schema.disabled = True
    updated_user_as_schema = repository.update(user_as_schema)
    return updated_user_as_schema


def authenticate_user(
    login_data: schemas.LoginPayload, repository: UserRepository
) -> schemas.User:
    try:
        user = _get_user_by_username(login_data.username, repository)
    except auth_errors.UserNotExistsError:
        raise auth_errors.AuthenticationFailedError(constants.USER_NOT_FOUND_DETAIL)

    # ensure the user is active
    if user.disabled:
        raise auth_errors.AuthenticationFailedError(constants.USER_DISABLED_DETAIL)

    # validate that the passwords match
    if not user.validate_password(login_data.password):
        raise auth_errors.AuthenticationFailedError(
            constants.USER_VALIDATION_FAILED_DETAIL
        )

    return user


def create_access_token(user: schemas.User, repository: UserRepository) -> JWToken:
    access_token_expires = timedelta(minutes=constants.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode: dict[str, Any] = {
        "sub": user.username,
        "scopes": [x for x in user.roles],
    }
    expire = datetime.now(timezone.utc) + access_token_expires
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, constants.JWT_SECRET_KEY, algorithm=constants.JWT_ALGORITHM
    )
    return encoded_jwt


def upgrade_user_to_admin(
    user: schemas.User, repository: UserRepository
) -> schemas.User:
    if rbac.ADMIN_ROLE in user.roles:
        raise ValueError("User is already an admin")
    user.roles.append(rbac.ADMIN_ROLE)
    updated_user = repository.update(user)
    return updated_user
