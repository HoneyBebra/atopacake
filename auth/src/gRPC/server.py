import grpc
from fastapi import HTTPException

from src.core.dependencies.jwt import get_access_token_data
from src.gRPC.protos import user_pb2, user_pb2_grpc


class GrpcServer(user_pb2_grpc.UserServicer):
    def __init__(self) -> None:
        super(GrpcServer, self).__init__()

    async def GetUserInfoByToken(
            self,
            request: user_pb2.GetUserInfoByTokenRequest,
            context: grpc.aio.ServicerContext,
    ) -> user_pb2.GetUserInfoByTokenResponse:
        try:
            user_data, token = get_access_token_data(request.access_token)
        except HTTPException:
            context.set_code(grpc.StatusCode.PERMISSION_DENIED)
            return user_pb2.GetUserInfoByTokenResponse()

        return user_pb2.GetUserInfoByTokenResponse(id=str(user_data.sub))
