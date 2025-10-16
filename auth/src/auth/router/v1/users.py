# TODO: make hybrid crypto system with RSA and AES

from fastapi import APIRouter, Depends, HTTPException, Response, Security, status
from fastapi_jwt import JwtAuthorizationCredentials

from src.auth.exceptions.users import InvalidCredentials, UserAlreadyExists

from src.auth.schemas.v1.users import UserJwtSchema, UserLoginSchema, UserRegisterSchema
from src.auth.services.users import UsersService
from src.core.config import settings
from src.auth.utils.handlers_decorators import CheckJWT

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
            "model": UserJwtSchema,
            "description": "User data received"
        },
        status.HTTP_403_FORBIDDEN: {
            "model": None,
            "description": "No rights",
        }
    },
)
@CheckJWT()
async def get_user(
    credentials: JwtAuthorizationCredentials = Security(settings.access_security),
) -> UserJwtSchema:
    return UserJwtSchema(**credentials.subject)


@router.post(
    "/refresh",
    description="Refresh tokens",
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
@CheckJWT()
async def refresh_access_token(
    user_service: UsersService = Depends(),
    credentials: JwtAuthorizationCredentials = Security(settings.refresh_security),
) -> Response:
    response = Response()
    return await user_service.refresh_token(credentials, response)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def invalidate_user(
    user_service: UserService = Depends(),
    refresh_credentials: JwtAuthorizationCredentials = Security(refresh_security),
    access_credentials: JwtAuthorizationCredentials = Security(access_security),
) -> None:
    user = await user_service.verify(refresh_credentials)

    await user_service.logout(user.id, refresh_credentials.jti, access_credentials.jti)
