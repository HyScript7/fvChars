from datetime import datetime, timedelta
from typing import Annotated, Dict

from fastapi import Header, HTTPException, status
from jose import ExpiredSignatureError, JWTError, jwt
from passlib.context import CryptContext

from ..config import APP_VERSION, JWT_SECRET
from ..database.models.user_model import (
    DisplaynameUpdate,
    PasswordUpdate,
    User,
    UserSignin,
    UserSignup,
)
from .errors.user_errors import (
    EmailAlreadyExistsError,
    ExpiredJWTError,
    InvalidCredentialsError,
    OutdatedJWTError,
    UserDoesntExistError,
    UsernameAlreadyExistsError,
    UserServiceError,
)

crypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

jwt_expires_in: timedelta = timedelta(hours=3)


async def required_get_current_user(jwt_token: Annotated[str, Header()]) -> User:
    """
    Retrieves the current user based on the provided JWT token.
    Raises a HTTPException if the user is not authenticated.

    Args:
        jwt_token (str | None, optional): The JWT token used to authenticate the user. Defaults to None.

    Returns:
        User
    """
    try:
        user = await get_current_user(jwt_token)
    except UserServiceError as e:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    if user is None:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail="You must be authenticated to use this route!",
        )
    return user


async def get_current_user(
    jwt_token: Annotated[str | None, Header()] = None
) -> User | None:
    """
    Retrieves the current user based on the provided JWT token.

    Args:
        jwt_token (str | None, optional): The JWT token used to authenticate the user. Defaults to None.

    Returns:
        User | None: The current user if the JWT token is valid and the user exists in the database. Returns None if guest.

    Raises:
        HTTPException: If the JWT token is invalid.
    """
    try:
        return await get_user_from_jwt(jwt_token)
    except UserServiceError as e:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


async def get_user_from_jwt(
    jwt_token: Annotated[str | None, Header()] = None
) -> User | None:
    """
    Retrieves the current user based on the provided JWT token.

    Args:
        jwt_token (str | None): The JWT token used to authenticate the user. Defaults to None if guest.

    Returns:
        User | None: The current user if the JWT token is valid and the user exists in the database. Returns None if guest.

    Raises:
        InvalidCredentialsError: If the JWT token is invalid.
        InvalidCredentialsError: If the JWT token is improperly formatted or the version in the payload does not match the current version.
        UserDoesntExistError: If the user with the userid specified in the payload does not exist in the database.
        ExpiredJWTError: If the JWT token has expired.
    """
    if jwt_token is None:
        return None
    try:
        payload: Dict[str | None] = jwt.decode(
            jwt_token, JWT_SECRET, algorithms=["HS256"]
        )
    except ExpiredSignatureError:
        raise ExpiredJWTError()
    except JWTError:
        raise OutdatedJWTError("None", APP_VERSION)
    if payload.get("username") is None:
        raise OutdatedJWTError(payload.get("v", "Unknown"), APP_VERSION)
    user: User | None = await User.find_one(User.username == payload["username"])
    if user is None:
        raise UserDoesntExistError(payload["username"] or "None")
    return user


async def create_jwt(user: User) -> str:
    """
    Encode a **new** JSON Web Token (JWT) for the user with the provided userid and version.

    Raises:
        UserDoesntExistError: If the user doesn't have an ID, but model instance exists.

    Returns:
        str: The encoded JWT token.
    """
    if user.id is None:
        raise UserDoesntExistError(user.username)
    token: str = jwt.encode(
        {
            "username": user.username,
            "v": APP_VERSION,
            "exp": datetime.now() + jwt_expires_in,
        },
        JWT_SECRET,
        algorithm="HS256",
    )
    return token


async def get_user_by_username(username: str) -> User:
    """Returns the user with the given username.

    Args:
        username (str): The username of the user to retrieve.

    Raises:
        UserDoesntExistError: If the user with the given username does not exist.

    Returns:
        User: The user with the given username.
    """
    user = await User.find_one(User.username == username)
    if user is None:
        raise UserDoesntExistError(username)
    return user


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
    if await User.find_one(User.username == user_signup.username.lower()) is not None:
        raise UsernameAlreadyExistsError(user_signup.username)
    if await User.find_one(User.email == user_signup.email.lower()) is not None:
        raise EmailAlreadyExistsError(user_signup.email)
    hashed_password = crypt_context.hash(user_signup.password)
    user = User(
        username=user_signup.username.lower(),
        password=hashed_password,
        email=user_signup.email.lower(),
        displayname=user_signup.displayname,
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
    user: User | None = await User.find_one(
        User.username == user_signin.username.lower()
    )
    if user is None:
        raise InvalidCredentialsError()
    if not crypt_context.verify(user_signin.password, user.password):
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
    await user.save()
    return user


async def update_password(user: User, password_update: PasswordUpdate) -> User:
    """
    Update the password of a user.

    Args:
        user (User): The user whose password is being updated.
        password_update (PasswordUpdate): An object containing the current and new passwords.

    Raises:
        InvalidCredentialsError: If the given current password is incorrect.

    Returns:
        User: The updated user.
    """
    if not crypt_context.verify(password_update.current_password, user.password):
        raise InvalidCredentialsError()
    user.password = crypt_context.hash(password_update.new_password)
    await user.save()
    return user


async def delete(user: User, user_password: str) -> None:
    """Deletes the given user.

    Args:
        user (User): The user to delete.
        user_password (str): The current (unhashed) password.

    Raises:
        InvalidCredentialsError: If the given current password is invalid.
    """
    if not crypt_context.verify(user_password, user.password):
        raise InvalidCredentialsError()
    await user.delete()
