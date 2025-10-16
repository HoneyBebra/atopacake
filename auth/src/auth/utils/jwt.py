import time
from datetime import timedelta
from typing import Literal

# TODO: jose is deprecated
from jose import jwt

from src.core.config import settings
from src.auth.exceptions.jwt import WrongTokenType


async def create_token(
        sub: str,
        email: str,
        phone_number: str,
        token_type: Literal["access", "refresh"],
) -> str:
    raw_data = {
        "sub": sub,
        "email": email,
        "phone_number": phone_number,
        "iat": time.time(),
    }

    if token_type == "access":
        raw_data["exp"] = timedelta(minutes=settings.access_token_expire_minutes)
    elif token_type == "refresh":
        raw_data["exp"] = timedelta(days=settings.refresh_token_expire_days)
    else:
        raise WrongTokenType

    to_encode = raw_data.copy()
    to_encode.update({"type": token_type})
    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    return encoded_jwt
