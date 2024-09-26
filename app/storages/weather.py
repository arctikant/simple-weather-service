from datetime import datetime

import orjson

from app.core.config import settings
from app.schemas.weather import WeatherData
from app.storages.base import BaseStorage


class WeatherStorage(BaseStorage):
    def _get_bucket_name(self) -> str:
        return 'weather'

    async def init(self) -> None:
        await self._s3_service.create_bucket(self._get_bucket_name())

    async def put(self, city: str, timestamp: datetime, data: WeatherData) -> str:
        bucket = self._get_bucket_name()
        key = f'{city}_{int(timestamp.timestamp())}.json'

        await self._s3_service.put(bucket=bucket, key=key, content=orjson.dumps(data.model_dump()))

        return f'{settings.AWS_ENDPOINT_URL}/{bucket}/{key}'

    async def get(self, key: str) -> WeatherData | None:
        try:
            json_data = await self._s3_service.get(bucket=self._get_bucket_name(), key=key)

            return WeatherData(**orjson.loads(json_data)) if json_data else None
        except ValueError:
            return None


weather_storage = WeatherStorage()
