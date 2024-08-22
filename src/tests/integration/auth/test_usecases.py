import uuid
from datetime import datetime
from datetime import timedelta
from datetime import timezone
from typing import Self

import pytest
from jose import jwt

from triangler_fastapi.auth import constants
from triangler_fastapi.auth import exceptions
from triangler_fastapi.auth import hashing
from triangler_fastapi.auth import schemas
from triangler_fastapi.auth import usecases


def create_user_create_schema() -> schemas.UserCreate:
    username = uuid.uuid4().hex
    test_user_create_schema = schemas.UserCreate.create(
        username=f"user_{username}",
        email=f"{username}@example.com",
        password="test",  # noqa: S106
    )
    return test_user_create_schema


class TestCreateUser:
    def test_create_user(self: Self) -> None:
        test_user_create_schema = create_user_create_schema()
        user = usecases.create_user_from_schema(test_user_create_schema)

        assert user is not None
        assert user.username == test_user_create_schema.username
        assert user.email == test_user_create_schema.email
        assert user.salt == test_user_create_schema.salt
        assert user.hashed_password == hashing.hash_password(
            password=test_user_create_schema.password, salt=test_user_create_schema.salt
        )

    def test_create_user_already_exists(self: Self) -> None:
        test_user_create_schema = create_user_create_schema()
        usecases.create_user_from_schema(test_user_create_schema)

        with pytest.raises(Exception) as e:
            usecases.create_user_from_schema(test_user_create_schema)
            assert test_user_create_schema.username in str(e.value)


class TestGetUser:
    def test_get_user(self: Self) -> None:
        test_user_create_schema = create_user_create_schema()

        test_user = usecases.create_user_from_schema(test_user_create_schema)
        user = usecases.get_user(test_user_create_schema.username)

        assert user is not None
        assert user.id == test_user.id
        assert user.email == test_user.email

    def test_get_user_not_found(self: Self) -> None:
        user = usecases.get_user("not found")

        assert user is None


class TestDisableUser:
    def test_disable_user(self: Self) -> None:
        test_user_create_schema = create_user_create_schema()

        test_user = usecases.create_user_from_schema(test_user_create_schema)
        user = usecases.disable_user(test_user.username)

        assert user is not None
        assert user.disabled is True

    def test_disable_user_not_found(self: Self) -> None:
        with pytest.raises(exceptions.UserNotExistsError) as e:
            usecases.disable_user("not found")
            assert constants.USER_NOT_FOUND_DETAIL in str(e.value)


class TestAuthenticateUser:
    def test_authenticate_user(self: Self) -> None:
        test_user_create_schema = create_user_create_schema()

        test_user = usecases.create_user_from_schema(test_user_create_schema)
        user = usecases.authenticate_user(
            schemas.LoginPayload(
                username=test_user.username,
                password="test",  # noqa: S106
            )
        )

        assert user is not None
        assert user.id == test_user.id
        assert user.email == test_user.email
        assert user.hashed_password == test_user.hashed_password
        assert user.salt == test_user.salt
        assert user.disabled == test_user.disabled
        assert user.roles == test_user.roles
        assert user.validate_password("test") is True
        assert user.validate_password("not test") is False

    def test_authenticate_user_not_found(self: Self) -> None:
        with pytest.raises(exceptions.AuthenticationFailedError) as e:
            usecases.authenticate_user(
                schemas.LoginPayload(
                    username="not found",
                    password="test",  # noqa: S106
                )
            )
            assert constants.USER_NOT_FOUND_DETAIL == str(e.value)

    def test_authenticate_user_disabled(self: Self) -> None:
        test_user_create_schema = create_user_create_schema()

        test_user = usecases.create_user_from_schema(test_user_create_schema)
        test_user = usecases.disable_user(test_user.username)

        with pytest.raises(exceptions.AuthenticationFailedError) as e:
            usecases.authenticate_user(
                schemas.LoginPayload(
                    username=test_user.username,
                    password="test",  # noqa: S106
                )
            )
            assert constants.USER_DISABLED_DETAIL == str(e.value)

    def test_authenticate_user_invalid_password(self: Self) -> None:
        test_user_create_schema = create_user_create_schema()

        test_user = usecases.create_user_from_schema(test_user_create_schema)

        with pytest.raises(exceptions.AuthenticationFailedError) as e:
            usecases.authenticate_user(
                schemas.LoginPayload(
                    username=test_user.username,
                    password="not test",  # noqa: S106
                )
            )
            assert constants.USER_VALIDATION_FAILED_DETAIL == str(e.value)


class TestCreateAccessToken:
    def test_create_access_token(self: Self) -> None:
        test_user_create_schema = create_user_create_schema()

        test_user = usecases.create_user_from_schema(test_user_create_schema)
        access_token = usecases.create_access_token(test_user)

        assert access_token is not None

        decoded_access_token = jwt.decode(
            access_token, constants.JWT_SECRET_KEY, algorithms=[constants.JWT_ALGORITHM]
        )
        access_token_expires = timedelta(
            minutes=constants.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
        )
        expire = datetime.now(timezone.utc) + access_token_expires

        assert decoded_access_token["sub"] == test_user.username
        assert decoded_access_token["scopes"] == [
            x for role in test_user.roles for x in role.scopes
        ]
        assert decoded_access_token["exp"] is not None
        assert decoded_access_token["exp"] > 0
        assert decoded_access_token["exp"] == pytest.approx(expire.timestamp())
