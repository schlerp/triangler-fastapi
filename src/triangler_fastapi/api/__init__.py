from fastapi import Depends
from fastapi import FastAPI

from triangler_fastapi import config
from triangler_fastapi.admin import admin
from triangler_fastapi.api.v1 import v1_router
from triangler_fastapi.auth import router as auth_router
from triangler_fastapi.persistence import get_db_session


def create_api() -> FastAPI:
    api = FastAPI(
        title="Triangler FastAPI",
        description="FastAPI implementation of Triangler.",
        version="0.1.0",
        dependencies=[Depends(get_db_session)],
        debug=config.DEBUG,
    )
    api.include_router(auth_router.router)
    api.include_router(v1_router)
    admin.mount_to(api)
    return api
