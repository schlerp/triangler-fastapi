from fastapi import FastAPI

from triangler_fastapi.api import create_api


def get_application() -> FastAPI:
    return create_api()
