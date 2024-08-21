class UserAlreadyExistsError(Exception):
    _message_template = "User '{username}' already exists"

    def __init__(self: "UserAlreadyExistsError", username: str) -> None:
        self.message = self._message_template.format(username=username)
        super().__init__(self.message)


class AuthenticationFailedError(Exception):
    def __init__(self: "AuthenticationFailedError", message: str) -> None:
        self.message = message
        super().__init__(self.message)


class UserNotExistsError(Exception):
    _message_template = "User '{username}' does not exist"

    def __init__(self: "UserNotExistsError", username: str) -> None:
        self.message = self._message_template.format(username=username)
        super().__init__(self.message)
