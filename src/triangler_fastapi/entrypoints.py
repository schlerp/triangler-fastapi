from fastapi import Depends
from fastapi import FastAPI

from triangler_fastapi import config
from triangler_fastapi.api import create_api_routes
from triangler_fastapi.persistence import get_db_session
from triangler_fastapi.views import create_view_routes


def get_application() -> FastAPI:
    app = FastAPI(
        title="Triangler FastAPI",
        description="FastAPI implementation of Triangler.",
        version="0.1.0",
        dependencies=[Depends(get_db_session)],
        debug=config.DEBUG,
    )

    # set up API routers
    app = create_api_routes(app)

    # set up view routers
    app = create_view_routes(app)

    return app
