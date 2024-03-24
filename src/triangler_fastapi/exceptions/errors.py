from triangler_fastapi.exceptions.base import TrianglerBaseError


class AuthenticationFailedError(TrianglerBaseError):
    """Raised when authentication fails."""


class AuthorizationFailedError(TrianglerBaseError):
    """Raised when authorization fails."""


class NotAuthenticatedError(TrianglerBaseError):
    """Raised when a user is not authenticated."""


class InvalidTokenError(TrianglerBaseError):
    """Raised when a token is invalid."""


class ObjectNotFoundError(TrianglerBaseError):
    """Raised when an object is not found."""


class ObjectAlreadyExistsError(TrianglerBaseError):
    """Raised when an object already exists."""
