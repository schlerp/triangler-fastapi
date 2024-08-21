from fastapi import APIRouter

from triangler_fastapi.api.v1 import experiment_router
from triangler_fastapi.api.v1 import observation_router

v1_router = APIRouter(
    prefix="/api/v1",
    tags=["v1"],
)
v1_router.include_router(experiment_router.router, tags=experiment_router.ROUTER_TAGS)
v1_router.include_router(observation_router.router, tags=observation_router.ROUTER_TAGS)
