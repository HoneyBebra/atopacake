import grpc
from fastapi import Cookie, Depends, HTTPException, status

from src.core.config import settings
from src.core.schemas import UserInfoByTokenSchema
from src.gRPC.client import GrpcClient, get_grpc_session


async def get_user_info_by_token(
    access_token: str | None = Cookie(default=None, alias=settings.access_token_key_in_cookie),
    grpc_session: GrpcClient = Depends(get_grpc_session),
) -> UserInfoByTokenSchema:
    await __check_raw_token(access_token)

    response = await __request_for_user_info(access_token, grpc_session)

    return await __get_user_data_from_response(response)


async def __check_raw_token(token: str | None) -> str:
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Credentials are not provided",
        )
    return token


async def __request_for_user_info(access_token: str, grpc_session: GrpcClient):  # TODO: Add type hint
    try:
        return await grpc_session.make_user_info_request(access_token=access_token)
    except grpc.RpcError as e:
        if e.code() == grpc.StatusCode.PERMISSION_DENIED:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=str(e)
            ) from e
        raise e


# TODO: Add type hint
async def __get_user_data_from_response(response) -> UserInfoByTokenSchema:
    print(response)
