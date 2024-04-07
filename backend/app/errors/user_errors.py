class EmailAlreadyTakenException(Exception):
    def __init__(self, email: str):
        super().__init__(f"User with email '{email}' already exists")


class UsernameAlreadyTakenException(Exception):
    def __init__(self, username: str):
        super().__init__(f"User with username '{username}' already exists")


class InvalidLogin(Exception):
    def __init__(self):
        super().__init__("Invalid credentials or token")


class UserNotFound(Exception):
    def __init__(self, username: str):
        super().__init__(f"User with username '{username}' was not found")
