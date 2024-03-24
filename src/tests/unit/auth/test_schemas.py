import datetime
from typing import Self

from triangler_fastapi.auth import hashing
from triangler_fastapi.auth import schemas


class TestRoleSchema:
    def test_role_has_scope(self: Self) -> None:
        """Test that a role has a scope."""
        role = schemas.Role(name="test", scopes=["test"])
        assert role.has_scope("test") is True

    def test_role_does_not_have_scope(self: Self) -> None:
        """Test that a role does not have a scope."""
        role = schemas.Role(name="test", scopes=["test"])
        assert role.has_scope("something else") is False


class TestUserSchema:
    @staticmethod
    def create_user(
        username: str = "test",
        id: int = 1,
        created_at: datetime.datetime = datetime.datetime(year=2000, month=1, day=1),
        email: str = "test@example.com",
        password: str = "test",  # noqa: S107
        salt: str = "salt",
        disabled: bool = False,
        roles: list[schemas.Role] = [schemas.Role(name="test", scopes=["test"])],
    ) -> schemas.User:
        """Create a user schema."""
        hashed_password = hashing.hash_password(password=password, salt=salt)
        return schemas.User(
            id=id,
            created_at=created_at,
            username=username,
            email=email,
            hashed_password=hashed_password,
            salt=salt,
            disabled=disabled,
            roles=roles,
        )

    def test_user_scopes_does_contain(self: Self) -> None:
        """Test that a user has a scope."""
        scopes = ["test", "test 2"]
        role = schemas.Role(name="test", scopes=scopes)
        user = self.create_user(roles=[role])
        assert all(scope in user.scopes for scope in scopes)

    def test_user_scopes_does_not_contain(self: Self) -> None:
        """Test that a user does not have a scope."""
        scopes = ["test", "test 2"]
        role = schemas.Role(name="test", scopes=scopes)
        user = self.create_user(roles=[role])

        assert any(scope not in user.scopes for scope in ["not me", "or me"])

    def test_validate_password_matches(self: Self) -> None:
        """Test that a user's password is validated."""
        password = "test"  # noqa: S105
        user = self.create_user(password=password)

        assert user.validate_password(password) is True

    def test_validate_password_doesnt_match(self: Self) -> None:
        """Test that a user's password is not validated."""
        password = "test"  # noqa: S105
        user = self.create_user(password=password)

        assert user.validate_password("something else") is False
