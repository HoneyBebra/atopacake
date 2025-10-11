from typing import Any

from jose import JWTError, jwt

# TODO: jose is deprecated
from src.auth.exceptions.jwt import InvalidTokenType, TokenValidationError
from src.auth.schemas.v1.users import UserJwtSchema
from src.core.config import settings


def create_token(data: UserJwtSchema, token_type: str) -> str:
    raw_data = dict(data)
    to_encode = raw_data.copy()
    to_encode.update({"type": token_type})
    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    return encoded_jwt


def verify_token(token: str, token_type: str) -> dict[str, Any]:
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=settings.jwt_algorithm)
        if payload.get("type") != token_type:
            raise InvalidTokenType
        return payload
    except JWTError as e:
        raise TokenValidationError from e
