class UsernameAlreadyExistsError(Exception):
    def __init__(self, username: str) -> None:
        super().__init__(f"The username '{username} is already taken!")


class EmailAlreadyExistsError(Exception):
    def __init__(self, email: str) -> None:
        super().__init__(f"The email '{email} is already  in use!")


class InvalidCredentialsError(Exception):
    def __init__(self) -> None:
        super().__init__("Incorrect username or password!")
