from fastapi import FastAPI

from triangler_fastapi.admin import admin
from triangler_fastapi.views import base as base_routes


def create_view_routes(app: FastAPI) -> FastAPI:
    """Create view routes for the FastAPI application."""
    app.include_router(base_routes.router)
    admin.mount_to(app)
    return app
