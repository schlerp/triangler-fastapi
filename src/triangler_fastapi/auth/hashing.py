import hashlib
from secrets import token_urlsafe

from triangler_fastapi.auth import constants


def generate_salt() -> str:
    """Generates a new cryptographically secure salt."""
    return token_urlsafe(constants.HASH_SALT_N_BYTES)


def hash_password(password: str, salt: str) -> str:
    """Hashes a password using the given salt."""
    return hashlib.pbkdf2_hmac(
        constants.HASH_ALGORITHM,
        password.encode("utf-8"),
        salt.encode("utf-8"),
        constants.HASH_ITERATIONS,
    ).hex()
