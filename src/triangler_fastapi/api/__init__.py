from fastapi import Depends
from fastapi import FastAPI

from triangler_fastapi import config
from triangler_fastapi.api.v1 import v1_router
from triangler_fastapi.data import persistence


def create_api() -> FastAPI:
    api = FastAPI(
        title="Triangler FastAPI",
        description="FastAPI implementation of Triangler.",
        version="0.1.0",
        dependencies=[Depends(persistence.get_db_session)],
        debug=config.DEBUG,
    )
    api.include_router(v1_router)
    return api
