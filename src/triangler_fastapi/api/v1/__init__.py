from fastapi import APIRouter

from triangler_fastapi.api.v1 import experiment_router

v1_router = APIRouter(
    prefix="/v1",
    tags=["v1"],
)
v1_router.include_router(
    experiment_router.router, tags=[experiment_router.EXPERIMENT_TAG]
)
