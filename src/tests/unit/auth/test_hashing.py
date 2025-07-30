from typing import Self

from triangler_fastapi.domain.auth import constants
from triangler_fastapi.domain.auth import hashing


class TestGenerateSalt:
    def test_generate_salt(self: Self) -> None:
        """Test that generate_salt returns a string of atleast the number of bytes."""
        salt = hashing.generate_salt()
        assert len(salt) > constants.HASH_SALT_N_BYTES
        assert isinstance(salt, str)

    def test_generate_salt_unique(self: Self) -> None:
        """Test that generate_salt returns unique salts."""
        salt1 = hashing.generate_salt()
        salt2 = hashing.generate_salt()
        assert salt1 != salt2


class TestHashPassword:
    def test_hash_password(self: Self) -> None:
        """Test that hash_password returns a string of the correct length."""
        password = "password"  # noqa: S105
        salt = hashing.generate_salt()
        hashed_password = hashing.hash_password(password, salt)
        hashed_password_again = hashing.hash_password(password, salt)
        assert isinstance(hashed_password, str)
        assert isinstance(hashed_password_again, str)
        assert hashed_password == hashed_password_again

    def test_hash_password_different_salts(self: Self) -> None:
        """Test that hash_password returns a string of the correct length."""
        password = "password"  # noqa: S105
        salt = hashing.generate_salt()
        other_salt = hashing.generate_salt()
        hashed_password = hashing.hash_password(password, salt)
        hashed_password_again = hashing.hash_password(password, other_salt)
        assert isinstance(hashed_password, str)
        assert isinstance(hashed_password_again, str)
        assert hashed_password != hashed_password_again
