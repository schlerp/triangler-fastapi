from triangler_fastapi.exceptions import errors


class UserAlreadyExistsError(errors.TrianglerBaseError):
    _message_template = "User '{username}' already exists"

    def __init__(self: "UserAlreadyExistsError", username: str) -> None:
        self.message = self._message_template.format(username=username)
        super().__init__(self.message)


class AuthenticationFailedError(errors.TrianglerBaseError):
    def __init__(self: "AuthenticationFailedError", message: str) -> None:
        self.message = message
        super().__init__(self.message)


class UserNotExistsError(errors.TrianglerBaseError):
    _message_template = "User '{username}' does not exist"

    def __init__(self: "UserNotExistsError", username: str) -> None:
        self.message = self._message_template.format(username=username)
        super().__init__(self.message)
