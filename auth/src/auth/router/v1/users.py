from fastapi import APIRouter, Cookie, Depends, HTTPException, Response, status
from jose import jwt

from src.auth.exceptions.users import InvalidCredentials, UserAlreadyExists
from src.auth.schemas.v1.users import (
    ResponseUserData,
    UserJwtSchema,
    UserLoginSchema,
    UserRegisterSchema,
)
from src.auth.services.users import UsersService
from src.auth.utils.handlers_decorators import CheckJWT
from src.core.config import settings

router = APIRouter(prefix="/users")


@router.post(
    "/signup",
    description="Creating user",
    summary="Validating fields -> "
            "Checking if user already created -> "
            "Creating user -> "
            "logging in user",
    responses={
        status.HTTP_204_NO_CONTENT: {
            "model": None,
            "description": "User created and logged in"
        },
        status.HTTP_409_CONFLICT: {
            "model": None,
            "description": "User already created",
        },
        # TODO: Check if ValueError
    },
)
async def signup_user(
        user_data: UserRegisterSchema,
        user_service: UsersService = Depends(),
) -> Response:
    try:
        response = Response()

        # TODO: rollback all if an error
        user = await user_service.create(user_data)
        response = await user_service.login(user, response)
        return response
    except UserAlreadyExists as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=e.message,
        ) from e


@router.post(
    "/login",
    description="Logging in user",
    summary="Validating fields -> Checking password -> Logging in user",
    responses={
        status.HTTP_204_NO_CONTENT: {
            "model": None,
            "description": "User logged in"
        },
        status.HTTP_401_UNAUTHORIZED: {
            "model": None,
            "description": "User didn't login"
        },
        # TODO: Check if ValueError
    },
)
async def login_user(
    login_data: UserLoginSchema,
    user_service: UsersService = Depends()
) -> Response:
    response = Response()
    try:
        user = await user_service.authenticate(login_data)
        response = await user_service.login(user, response)
    except InvalidCredentials as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.message,
        ) from e

    return response


@router.get(
    "/me",
    description="Get user data",
    summary="Read user data from DB",
    responses={
        status.HTTP_200_OK: {
            "model": ResponseUserData,
            "description": "User data received"
        },
        status.HTTP_403_FORBIDDEN: {
            "model": None,
            "description": "No rights",
        }
    },
)
@CheckJWT("access")
async def get_user(
    access_credentials: str | None = Cookie(
        default=None,
        alias=settings.access_token_key_in_cookie,
    ),
) -> ResponseUserData:
    # TODO: Convert decorator to DI to avoid duplicating payload calculations
    payload = jwt.decode(
        token=access_credentials,
        key=settings.jwt_secret_key,
        algorithms=settings.jwt_algorithm,
    )

    return {
        "id": payload.get("sub"),
        "email": payload.get("email"),
        "phone_number": payload.get("phone_number"),
    }


@router.post(
    "/refresh",
    description="Refresh access token",
    summary="Get new access token and replace refresh one",
    responses={
        status.HTTP_200_OK: {
            "model": UserJwtSchema,
            "description": "User data received"
        },
        status.HTTP_403_FORBIDDEN: {
            "model": None,
            "description": "No rights",
        }
    },
)
@CheckJWT("refresh")
async def refresh_access_token(
    user_service: UsersService = Depends(),
    refresh_credentials: str | None = Cookie(
        default=None,
        alias=settings.refresh_token_key_in_cookie,
    ),
) -> Response:
    response = Response()

    # TODO: Convert decorator to DI to avoid duplicating payload calculations
    payload = jwt.decode(
        token=refresh_credentials,
        key=settings.jwt_secret_key,
        algorithms=settings.jwt_algorithm,
    )

    await user_service.add_token_to_blacklist(refresh_credentials)
    return await user_service.refresh_token(payload, response)


@router.post(
    "/logout",
    description="Logout user",
    summary="Logout user -> Add tokens to blacklist",
    responses={
        status.HTTP_200_OK: {
            "model": None,
            "description": "User invalidated"
        },
        status.HTTP_403_FORBIDDEN: {
            "model": None,
            "description": "No rights",
        }
    },
)
@CheckJWT("all")
async def logout_user(
    user_service: UsersService = Depends(),
    refresh_credentials: str | None = Cookie(
        default=None,
        alias=settings.refresh_token_key_in_cookie,
    ),
    access_credentials: str | None = Cookie(
        default=None,
        alias=settings.access_token_key_in_cookie,
    ),
) -> None:
    await user_service.add_token_to_blacklist(access_credentials)
    await user_service.add_token_to_blacklist(refresh_credentials)
