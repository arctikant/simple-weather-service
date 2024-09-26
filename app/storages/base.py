from abc import ABC, abstractmethod

from app.core.aws.s3 import S3Service


class BaseStorage(ABC):
    def __init__(self) -> None:
        self._s3_service = S3Service()

    @abstractmethod
    def _get_bucket_name(self) -> str:
        raise NotImplementedError

    async def init(self) -> None:
        await self._s3_service.create_bucket(self._get_bucket_name())
