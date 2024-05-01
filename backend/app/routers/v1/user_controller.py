from fastapi import HTTPException, status, Depends, APIRouter
from ...database.models import user_model
from ...services import user_service
from ...services.errors import user_errors
from ...schemas import generic_responses

user_controller: APIRouter = APIRouter(prefix="/users")


# TODO: Return current session info here instead. Consider renaming to /self, /me or /whoami
@user_controller.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=generic_responses.GenericMessageResponse,
)
async def root():
    return {"message": "Hello World"}


@user_controller.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=user_model.UserPublic,
    responses={409: {"model": generic_responses.GenericHTTPException}},
)
async def register(user_signup: user_model.UserSignup):
    try:
        user: user_model.User = await user_service.register(user_signup)
    except user_errors.EmailAlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except user_errors.UsernameAlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    return user


@user_controller.post(
    "/login",
    status_code=status.HTTP_200_OK,
    response_model=user_model.UserPublic,
    responses={401: {"model": generic_responses.GenericHTTPException}},
)
async def login(user_signin: user_model.UserSignin):
    try:
        user: user_model.User = await user_service.login(user_signin)
    except user_errors.InvalidCredentialsError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    return user


@user_controller.post(
    "/delete",
    status_code=status.HTTP_200_OK,
    response_model=generic_responses.GenericMessageResponse,
    responses={
        401: {"model": generic_responses.GenericHTTPException},
        404: {"model": generic_responses.GenericHTTPException},
    },
)
async def delete(user_credentials: user_model.UserSignin):
    # TODO: Get the current user using a session instead of provided credentials.
    try:
        user: user_model.User = await user_service.get_user_by_username(
            user_credentials.username
        )
    except user_errors.UserDoesntExistError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    try:
        await user_service.delete(user, user_credentials.password)
    except user_errors.InvalidCredentialsError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    return {"message": "User deleted"}


@user_controller.put(
    "/update/displayname",
    status_code=status.HTTP_200_OK,
    response_model=user_model.UserPublic,
    responses={404: {"model": generic_responses.GenericHTTPException}},
)
async def update(
    displayname_update: user_model.DisplaynameUpdate,
    user_credentials: user_model.UserSignin,
):
    # TODO: Get the current user using a session instead of provided credentials.
    try:
        user: user_model.User = await user_service.get_user_by_username(
            user_credentials.username
        )
    except user_errors.UserDoesntExistError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    return await user_service.update_displayname(user, displayname_update)


@user_controller.post(
    "/update/password",
    status_code=status.HTTP_200_OK,
    response_model=user_model.UserPublic,
    responses={
        401: {"model": generic_responses.GenericHTTPException},
        404: {"model": generic_responses.GenericHTTPException},
    },
)
async def update(
    password_update: user_model.PasswordUpdate,
    user_credentials: user_model.UserSignin,
):
    # TODO: Get the current user using a session instead of provided credentials.
    try:
        user: user_model.User = await user_service.get_user_by_username(
            user_credentials.username
        )
    except user_errors.UserDoesntExistError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    try:
        return await user_service.update_password(user, password_update)
    except user_errors.InvalidCredentialsError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
