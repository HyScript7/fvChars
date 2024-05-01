from fastapi import APIRouter, Depends, HTTPException, status

from ...database.models import user_model
from ...schemas import generic_responses, user_responses
from ...services import user_service
from ...services.errors import user_errors

user_controller: APIRouter = APIRouter(prefix="/users")


@user_controller.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=generic_responses.GenericMessageResponse,
)
async def root(
    current_user: user_model.User = Depends(user_service.get_current_user),
):
    if current_user is None:
        return {"message": "Hello Guest"}
    return {"message": f"Hello {current_user.name}"}


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
    response_model=user_responses.JWTResponse,
    responses={401: {"model": generic_responses.GenericHTTPException}},
)
async def login(user_signin: user_model.UserSignin):
    try:
        user: user_model.User = await user_service.login(user_signin)
    except user_errors.InvalidCredentialsError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    return {"token": await user_service.create_jwt(user)}


@user_controller.post(
    "/delete",
    status_code=status.HTTP_200_OK,
    response_model=generic_responses.GenericMessageResponse,
    responses={
        401: {"model": generic_responses.GenericHTTPException},
        404: {"model": generic_responses.GenericHTTPException},
    },
)
async def delete(
    current_password: str,
    current_user: user_model.User = Depends(user_service.required_get_current_user),
):
    try:
        await user_service.delete(current_user, current_password)
    except user_errors.InvalidCredentialsError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You must provide a correct current password to delete your account.",
        )
    return {"message": "User deleted successfully"}


@user_controller.put(
    "/update/displayname",
    status_code=status.HTTP_200_OK,
    response_model=user_model.UserPublic,
    responses={404: {"model": generic_responses.GenericHTTPException}},
)
async def update(
    displayname_update: user_model.DisplaynameUpdate,
    current_user: user_model.User = Depends(user_service.required_get_current_user),
):
    return await user_service.update_displayname(current_user, displayname_update)


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
    current_user: user_model.User = Depends(user_service.required_get_current_user),
):
    try:
        return await user_service.update_password(current_user, password_update)
    except user_errors.InvalidCredentialsError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
