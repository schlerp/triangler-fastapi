from fastapi import FastAPI

from triangler_fastapi.admin import admin
from triangler_fastapi.api.v1 import v1_router
from triangler_fastapi.auth import router as auth_router


def create_api_routes(app: FastAPI) -> FastAPI:
    """Create API routes for the FastAPI application."""
    app.include_router(auth_router.router)
    app.include_router(v1_router)
    admin.mount_to(app)
    return app
