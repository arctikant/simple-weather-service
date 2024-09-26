from typing import Any

from app.core.aws.base import BaseService
from app.core.logging import logger
from app.exceptions import S3ServiceError


class S3Service(BaseService):
    def _get_service_name(self):
        return 's3'

    async def create_bucket(self, name: str) -> None:
        async for client in self._get_client():
            try:
                await client.create_bucket(Bucket=name)
            except Exception as e:
                logger.exception(f"Error creating bucket '{name}': {e}")
                raise S3ServiceError(f"Error creating bucket '{name}': {e}")

    async def get(self, bucket: str, key: str) -> Any | None:
        async for client in self._get_client():
            try:
                response = await client.get_object(Bucket=bucket, Key=key)
                async with response['Body'] as stream:
                    data = await stream.read()

                return data
            except client.exceptions.NoSuchKey:
                raise S3ServiceError(f"The specified key '{key}' does not exist in bucket '{bucket}'.")

        return None

    async def put(self, bucket: str, key: str, content: Any) -> None:
        async for client in self._get_client():
            await client.put_object(Bucket=bucket, Key=key, Body=content)

    async def delete(self, bucket: str, key: str) -> None:
        async for client in self._get_client():
            response = await client.delete_object(Bucket=bucket, Key=key)

            return response
