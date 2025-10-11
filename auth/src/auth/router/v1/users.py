# TODO: make hybrid crypto system with RSA and AES

from fastapi import APIRouter, Depends, HTTPException, Response, Security, status
from fastapi_jwt import JwtAuthorizationCredentials

from src.auth.exceptions.users import (
    InvalidCredentials,
    NoCredentialsData,
    TokenInBlackList,
    UserAlreadyExists,
)
from src.auth.schemas.v1.users import UserJwtSchema, UserLoginSchema, UserRegisterSchema
from src.auth.services.users import UsersService
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
    },
)
async def get_user(
    user_service: UsersService = Depends(),
    credentials: JwtAuthorizationCredentials = Security(settings.access_security),
) -> UserJwtSchema:
    try:
        user = await user_service.verify_jwt(credentials)
        return user
    except (NoCredentialsData, TokenInBlackList) as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=e.message,
        ) from e


"""
@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
        token_data: TokenRefresh,
        session: AsyncSession = Depends(get_session)
):
    payload = verify_token(token_data.refresh_token, "refresh")
    user_id = payload.get("sub")

    # Проверка refresh токена в БД
    tokens_repository = RefreshTokensRepository(session)
    token_record = await tokens_repository.get_by_token(token_data.refresh_token)

    if not token_record or token_record.is_revoked:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )

    # Создание нового access токена
    access_token = create_access_token(data={"sub": user_id})

    return TokenResponse(
        access_token=access_token,
        refresh_token=token_data.refresh_token,  # Refresh токен остается тот же
        expires_in=settings.access_token_expire_minutes * 60
    )


@router.post("/logout")
async def logout(
        token_data: TokenRefresh,
        session: AsyncSession = Depends(get_session)
):
    tokens_repository = RefreshTokensRepository(session)
    await tokens_repository.revoke_token(token_data.refresh_token)

    return {"message": "Successfully logged out"}
"""
