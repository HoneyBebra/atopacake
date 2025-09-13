from typing import Any

from jose import JWTError, jwt

from src.auth.exceptions.jwt import InvalidTokenType, TokenValidationError
from src.core.config import settings


def create_token(data: dict[str, Any], token_type: str) -> str:
    to_encode = data.copy()
    to_encode.update({"type": token_type})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt


def verify_token(token: str, token_type: str) -> dict[str, Any]:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=settings.algorithm)
        if payload.get("type") != token_type:
            raise InvalidTokenType
        return payload
    except JWTError as e:
        raise TokenValidationError from e
