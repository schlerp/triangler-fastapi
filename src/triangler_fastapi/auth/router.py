from typing import Annotated

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from triangler_fastapi.auth import constants
from triangler_fastapi.auth import depends
from triangler_fastapi.auth import schemas
from triangler_fastapi.auth import usecases
from triangler_fastapi.exceptions import errors

router = APIRouter(
    prefix=constants.ROUTER_PREFIX,
    tags=["Auth", "v1"],
    responses={404: {"description": "Not found"}},
)


@router.post(constants.TOKEN_PATH)
async def login_for_access_token(
    login_data: schemas.LoginPayload,
) -> schemas.Token:
    try:
        user = usecases.authenticate_user(login_data=login_data)
    except errors.AuthenticationFailedError as e:
        raise HTTPException(status_code=400, detail=str(e))

    access_token = usecases.create_access_token(user=user)
    return schemas.Token(access_token=access_token, token_type="bearer")  # noqa: S106


@router.get("/users/me/", response_model=schemas.User)
async def read_users_me(
    current_user: Annotated[schemas.User, Depends(depends.get_current_active_user)],
) -> schemas.User:
    return current_user
