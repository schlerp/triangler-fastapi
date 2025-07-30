from fastapi.security import OAuth2PasswordBearer

from triangler_fastapi.domain.auth import constants
from triangler_fastapi.domain.auth.schemas import Role

SCOPES: dict[str, str] = {
    "me": "Read information about the current user.",
    # experiment scopes
    "read_experiments": "Read experiments.",
    "write_experiments": "Add/update experiments.",
    "admin_experiments": "Perform all actions on experiments.",
    # observation scopes
    "read_observations": "Read observations.",
    "write_observations": "Add/update observations.",
    "admin_observations": "Perform all actions on observations.",
    "anonymous": "Perform actions as an anonymous user",
}


ADMIN_ROLE = Role(name="admin", scopes=[x for x in SCOPES.keys()])
STAFF_ROLE = Role(
    name="staff",
    scopes=[
        "me",
        "read_experiments",
        "read_observations",
        "write_experiments",
        "write_observations",
    ],
)
ANONYMOUS_ROLE = Role(name="anonymous", scopes=["anonymous"])


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=constants.TOKEN_PATH_ABSOLUTE, scopes=SCOPES
)
