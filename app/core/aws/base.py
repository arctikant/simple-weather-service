from abc import ABC, abstractmethod
from collections.abc import AsyncGenerator

from aiobotocore.client import AioBaseClient
from aiobotocore.session import get_session

from app.core.config import settings

session = get_session()


class BaseService(ABC):
    @abstractmethod
    def _get_service_name(self):
        raise NotImplementedError

    async def _get_client(self) -> AsyncGenerator[AioBaseClient, None]:
        async with session.create_client(
            self._get_service_name(),
            region_name=settings.AWS_REGION_NAME,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_ACCESS_KEY_SECRET,
            endpoint_url=settings.AWS_ENDPOINT_URL,
            use_ssl=False,
        ) as client:
            yield client
