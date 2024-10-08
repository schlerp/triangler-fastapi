import os
import tempfile

from loguru import logger


def env_bool(name: str, default: bool = False) -> bool:
    """Get an environment variable as a boolean."""
    var = os.environ.get(name, None)
    if var is None:
        return default
    return var.lower() in ("true", "y", "yes")


DEBUG = os.environ.get("DEBUG", "False").lower() in ("true", "y", "yes")
IS_PROD = os.environ.get("IS_PROD", "False").lower() in ("true", "y", "yes")

# get our database URL
SQLALCHEMY_DATABASE_URL = os.environ.get("SQLALCHEMY_DATABASE_URL", None)
if SQLALCHEMY_DATABASE_URL is None:
    database_path = os.path.join(tempfile.mkdtemp(), "triangler_test.db")
    SQLALCHEMY_DATABASE_URL = f"sqlite:///{database_path}"
    logger.warning(f"SQLALCHEMY_DATABASE_URL not set, using {SQLALCHEMY_DATABASE_URL}")

if DEBUG:
    logger.debug(f"{SQLALCHEMY_DATABASE_URL=}")

# get our HOSTNAME
HOST_NAME = os.environ.get("HOST_NAME", "triangler.example.com")

if DEBUG:
    logger.debug(f"{HOST_NAME=}")

# set our observation token parameters
OBSERVATION_TOKEN_LENGTH = 6
OBSERVATION_TOKEN_EXPIRY_DAYS = 7
