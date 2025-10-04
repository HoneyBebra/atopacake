from fastapi import APIRouter, Depends, HTTPException, Response, status

from src.auth.exceptions.users import UserAlreadyExists
from src.auth.schemas.v1.users import UserRegisterSchema
from src.auth.services.users import UsersService

router = APIRouter(prefix="/users")


@router.post(
    "/register",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Register and creating user",
    summary="Register and creating user",
    responses={
        status.HTTP_204_NO_CONTENT: {
            "model": None,
            "description": "User created",
        },
        status.HTTP_409_CONFLICT: {
            "model": None,
            "description": "User already created",
        },
    },
)
async def register_user(
        user_data: UserRegisterSchema,
        user_service: UsersService = Depends(),
) -> Response:
    response = Response()
    try:
        return await user_service.register(user_data, response)
    except UserAlreadyExists as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=e.message,
        ) from e


"""
@router.post("/login", response_model=TokenResponse)
async def login(
        user_data: UserLogin,
        session: AsyncSession = Depends(get_session)
):
    user_repository = UsersRepository(session)
    user = await user_repository.get_by_login(user_data.login)

    if not user or not verify_password(user_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect login or password"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )

    # Создание токенов
    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})

    # Сохранение refresh токена
    tokens_repository = RefreshTokensRepository(session)
    await tokens_repository.create({
        "token": refresh_token,
        "user_id": user.id,
        "expires_at": datetime.utcnow() + timedelta(days=settings.refresh_token_expire_days)
    })

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=settings.access_token_expire_minutes * 60
    )


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
