from typing import Annotated
from typing import cast

from fastapi import Depends
from fastapi import HTTPException
from fastapi import Security
from fastapi import status
from fastapi.security import SecurityScopes
from jose import JWTError
from jose import jwt
from pydantic import ValidationError

from triangler_fastapi.domain.auth import constants
from triangler_fastapi.domain.auth import rbac
from triangler_fastapi.domain.auth import schemas as auth_schemas
from triangler_fastapi.domain.auth import usecases
from triangler_fastapi.exceptions import errors


async def get_current_user(
    security_scopes: SecurityScopes, token: Annotated[str, Depends(rbac.oauth2_scheme)]
) -> auth_schemas.User:
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    try:
        payload: auth_schemas.TokenPayload = cast(
            auth_schemas.TokenPayload,
            cast(
                object,
                jwt.decode(
                    token,
                    key=constants.JWT_SECRET_KEY,
                    algorithms=[constants.JWT_ALGORITHM],
                ),
            ),
        )
        username = payload.sub

        token_scopes = payload.scopes
    except (JWTError, ValidationError):
        raise errors.InvalidTokenError("JWT token provided was invalid!")

    user = usecases.get_user(username=username)
    if user is None:
        raise credentials_exception

    for scope in security_scopes.scopes:
        if scope not in token_scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )
    return user


async def get_current_active_user(
    current_user: Annotated[
        auth_schemas.User, Security(get_current_user, scopes=["me"])
    ],
) -> auth_schemas.User:
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
