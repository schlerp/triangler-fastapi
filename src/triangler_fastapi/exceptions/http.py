from fastapi import HTTPException
from loguru import logger

from triangler_fastapi import config
from triangler_fastapi.exceptions.base import TrianglerBaseError
from triangler_fastapi.exceptions.mapping import HTTP_EXCEPTION_CODE_MAP


def throw_http_exception(e: TrianglerBaseError) -> None:
    """Raises an HTTP exception based on the exception type."""
    status_code = HTTP_EXCEPTION_CODE_MAP.get(type(e), 500)
    if config.DEBUG:
        message_template = (
            "Raising HTTP exception from {} with status code {}.\n"
            "message: {}\n"
            "details: {}"
        )
        logger.error(message_template, type(e), status_code, e)
    raise HTTPException(status_code=status_code, detail=str(e))
