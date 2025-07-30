from fastapi import APIRouter

from triangler_fastapi.api.v1 import auth
from triangler_fastapi.api.v1 import experiments

v1_router = APIRouter(
    prefix="/api/v1",
    tags=["v1"],
)
v1_router.include_router(experiments.router, tags=experiments.ROUTER_TAGS)
v1_router.include_router(auth.router, tags=auth.ROUTER_TAGS)
