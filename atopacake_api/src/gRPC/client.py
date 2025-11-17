from typing import AsyncGenerator

import grpc

from src.core.config import settings
from src.gRPC.protos import user_pb2, user_pb2_grpc


class GrpcClient:
    def __init__(self) -> None:
        self.channel = None
        self.stub = None

    async def __aenter__(self) -> "GrpcClient":
        self.channel = grpc.aio.insecure_channel(settings.grpc_user_service_url)
        self.stub = user_pb2_grpc.UserStub(self.channel)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:  # type: ignore[no-untyped-def]
        if self.channel:
            await self.channel.close()

    async def make_user_info_request(  # type: ignore[no-untyped-def]
            self,
            access_token: str,
    ):
        request = user_pb2.GetUserInfoByTokenRequest(access_token=access_token)
        return await self.stub.GetUserInfoByToken(request)


async def get_grpc_session() -> AsyncGenerator:
    async with GrpcClient() as session:
        yield session
