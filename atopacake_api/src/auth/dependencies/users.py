from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.auth.models.users import Users
from src.auth.services.repositories.users import UsersRepository
from src.auth.utils.jwt import verify_token


async def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer),
        user_repository: UsersRepository = Depends(),
) -> Users:
    token = credentials.credentials
    payload = verify_token(token, "access")

    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )

    user = await user_repository.read(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    return user
