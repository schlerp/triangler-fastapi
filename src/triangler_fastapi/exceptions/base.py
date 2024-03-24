from typing import Any
from typing import Optional
from typing import Self


class TrianglerBaseError(Exception):
    """Base class for all exceptions in Triangler"""

    def __init__(
        self: Self, message: str, details: Optional[dict[str, Any]] = None
    ) -> None:
        self.message = message
        self.details = details

    def __str__(self: Self) -> str:
        return self.message
