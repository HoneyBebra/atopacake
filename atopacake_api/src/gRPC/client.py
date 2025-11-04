'''
import grpc
from google.protobuf import empty_pb2

from src.protos import user_service_pb2, user_service_pb2_grpc
from src.core.config import settings


class UserServiceClient:
    def __init__(self):
        self.channel = None
        self.stub = None

    # TODO: make context manager and return as DB object
    async def connect(self):
        """Подключаемся к gRPC серверу"""
        self.channel = grpc.aio.insecure_channel(settings.grpc_user_service_url)
        self.stub = user_service_pb2_grpc.UserServiceStub(self.channel)

    async def validate_token(self, token: str) -> dict:
        """Валидируем токен - аналог POST /auth/validate"""
        request = user_service_pb2.TokenRequest(token=token)
        try:
            response = await self.stub.ValidateToken(request)
            return {
                "id": response.id,
                "username": response.username,
                "email": response.email,
                "is_active": response.is_active
            }
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.UNAUTHENTICATED:
                return None
            raise e

    async def get_user_info(self, user_id: str) -> dict:
        """Получаем информацию о пользователе - аналог GET /users/{user_id}"""
        request = user_service_pb2.UserRequest(user_id=user_id)
        response = await self.stub.GetUserInfo(request)
        return {
            "id": response.id,
            "username": response.username,
            "email": response.email
        }

    async def close(self):
        """Закрываем соединение"""
        if self.channel:
            await self.channel.close()


# Создаем глобальный экземпляр клиента
user_client = UserServiceClient()
'''
