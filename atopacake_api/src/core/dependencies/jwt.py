import grpc
from fastapi import HTTPException, status, Cookie

from src.core.config import settings
from src.gRPC.protos import user_pb2, user_pb2_grpc
from src.core.schemas import UserInfoByTokenSchema


async def get_user_info_by_token(
    access_token: str | None = Cookie(default=None, alias=settings.access_token_key_in_cookie)
) -> UserInfoByTokenSchema:
    await __check_raw_token(access_token)

    # user_info = await __request_for_user_info()


async def __check_raw_token(token: str | None) -> str:
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Credentials are not provided",
        )
    return token


"""
async def __request_for_user_info() -> UserInfoByTokenSchema:
    async with grpc.aio.insecure_channel(settings.grpc_auth_url) as channel:
        stub = user_pb2_grpc.UserStub(channel)
        req = user_pb2.GetUserInfoByTokenRequest(token=access_token)
        try:
            await stub.GetInfoByToken(req)
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.PERMISSION_DENIED:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN) from e
            raise e
"""
