from ..database.models.user_model import (
    User,
    UserSignin,
    UserSignup,
    DisplaynameUpdate,
    PasswordUpdate,
)
from .errors.user_errors import (
    EmailAlreadyExistsError,
    InvalidCredentialsError,
    UsernameAlreadyExistsError,
)


async def register(user_signup: UserSignup) -> User:
    """Registers a new user with the given signup data.

    Args:
        user_signup (UserSignup): The signup data for the new user.

    Raises:
        UsernameAlreadyExistsError: If a user with the given username already exists.
        EmailAlreadyExistsError: If a user with the given email already exists.

    Returns:
        User: The newly registered user.
    """
    if User.find_one(username=user_signup.username.lower()) is not None:
        raise UsernameAlreadyExistsError(user_signup.username)
    if User.find_one(email=user_signup.email.lower()) is not None:
        raise EmailAlreadyExistsError(user_signup.email)
    # TODO: Use passlib to hash password with salt
    user = User(
        username=user_signup.username.lower(),
        displayname=user_signup.displayname,
        email=user_signup.email.lower(),
        password=user_signup.password,
    )
    await user.insert()
    return user


async def login(user_signin: UserSignin) -> User:
    """Logs in a user with the given signin data.

    Args:
        user_signin (UserSignin): The signin data for the user.

    Raises:
        InvalidCredentialsError: If the given credentials are invalid.

    Returns:
        User: The logged in user.
    """
    user: User | None = User.find_one(username=user_signin.username.lower())
    if user is None:
        raise InvalidCredentialsError()
    # TODO: Use passlib and salted hashes for password validation
    if user.password != user_signin.password:
        raise InvalidCredentialsError()
    return user


async def update_displayname(user: User, displayname_update: DisplaynameUpdate) -> User:
    """
    Update the given user with the provided display name update.

    Args:
        user (User): The user to update.
        displayname_update (DisplaynameUpdate): The display name update data.

    Returns:
        User: The updated user.
    """
    if displayname_update.displayname is not None:
        user.displayname = displayname_update.displayname
    await user.update()
    return user


async def update_password(user: User, password_update: PasswordUpdate) -> User:
    # TODO: Use passlib and salted hashes for password validation
    if password_update.current_password != password_update.new_password:
        raise InvalidCredentialsError()
    # TODO: Use passlib to hash password with salt
    user.password = password_update.new_password
    await user.update()
    return user


async def delete(user: User, user_password: str) -> None:
    """Deletes the given user.

    Args:
        user (User): The user to delete.
        user_update (UserUpdate): The update data containing the current password.

    Raises:
        InvalidCredentialsError: If the given current password is invalid.
    """
    # TODO: Use passlib and salted hashes for current password validation
    if user.password != user_password.current_password:
        raise InvalidCredentialsError()
    await user.delete()
