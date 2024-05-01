from typing import Optional


class UserServiceError(Exception):
    """
    An exception that can occour while using the User Service.
    Usage: raise UserServiceException()
    """

    ...


class UsernameAlreadyExistsError(UserServiceError):
    def __init__(self, username: str) -> None:
        super().__init__(f"The username '{username}' is already taken!")


class EmailAlreadyExistsError(UserServiceError):
    def __init__(self, email: str) -> None:
        super().__init__(f"The email '{email}' is already  in use!")


class InvalidCredentialsError(UserServiceError):
    def __init__(self, msg: Optional[str] = None) -> None:
        super().__init__(msg or "Incorrect username or password!")


class UserDoesntExistError(UserServiceError):
    """An exception that can occour when attempting to delete or update a user.
    Usage: raise UserDoesntExistError("foobar")
    """

    def __init__(self, id: str) -> None:
        super().__init__(f"User '{id}' does not exist!")


class InvalidJWTError(UserServiceError):
    """
    An exception that can occour while using the User Service to decode a JWT.
    Usage: raise InvalidJWTError()
    """

    ...


class ExpiredJWTError(UserServiceError):
    def __init__(self) -> None:
        super().__init__(
            "The provided JWT token has expired! Please login again and use the new token."
        )


class OutdatedJWTError(UserServiceError):
    def __init__(self, token_ver: str, server_ver: str) -> None:
        super().__init__(
            f"The provided JWT token appears to be corrupted. Is an instance outdated? Your token version is {token_ver}, and the server version is {server_ver}!"
        )
