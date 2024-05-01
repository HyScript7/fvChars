class UserServiceError(Exception):
    """
    An exception that can occour while using the User Service.
    Usage: raise UserServiceException()
    """
    ...


class UsernameAlreadyExistsError(UserServiceError):
    def __init__(self, username: str) -> None:
        super().__init__(f"The username '{username} is already taken!")


class EmailAlreadyExistsError(UserServiceError):
    def __init__(self, email: str) -> None:
        super().__init__(f"The email '{email} is already  in use!")


class InvalidCredentialsError(UserServiceError):
    def __init__(self) -> None:
        super().__init__("Incorrect username or password!")
