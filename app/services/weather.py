from datetime import UTC, datetime
from enum import Enum

import httpx
from fastapi import status

from app.core.config import settings
from app.core.logging import logger
from app.exceptions import DynamoDBServiceError, S3ServiceError, WeatherServiceError
from app.repositories.weather_event import weather_event_repository
from app.schemas.weather import WeatherData, WeatherEvent
from app.storages.weather import weather_storage


class OpenWeatherCode(Enum):
    SUCCESS: int = 200
    NOT_FOUND: int = 404


class WeatherService:
    async def get_weather(self, city) -> WeatherData:
        # Check if the cached data exists in specified period
        event = await weather_event_repository.get_last_for_period(
            city=city, seconds=settings.WEATHER_CACHE_TTL_SECONDS
        )
        data = None

        if event:
            # Try to get cached data from the storage
            try:
                data = await weather_storage.get(event.s3_url.split('/')[-1])
            except S3ServiceError as e:
                logger.exception(f"Can't get cached weather data from the storage: {e}")

        if data is None:
            # Fetch from Open Weather service
            data = await self._get_from_open_weather(city)

            # Store data to S3
            timestamp = datetime.now(UTC)
            url = await weather_storage.put(city=city, timestamp=timestamp, data=data)

            # Try to store event log
            try:
                await weather_event_repository.put(WeatherEvent(city=city, timestamp=timestamp, s3_url=url))
            except DynamoDBServiceError as e:
                logger.exception(f"Can't store weather event log to DB: {e}")

        return data

    async def _get_from_open_weather(self, city) -> WeatherData:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    settings.OPEN_WEATHER_URL,
                    params={
                        'q': city,
                        'appid': settings.OPEN_WEATHER_API_KEY,
                        'units': 'metric',
                    },
                )
            except httpx.RequestError as e:
                raise WeatherServiceError(
                    f'Request to weather service failed: {str(e)}',
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                )

            data = response.json()

            if int(data['cod']) == OpenWeatherCode.NOT_FOUND.value:
                raise WeatherServiceError('City not found', status_code=status.HTTP_404_NOT_FOUND)

            if 'main' not in data:
                raise WeatherServiceError(
                    'Invalid response from weather service',
                    status_code=status.HTTP_400_BAD_REQUEST,
                )

            return WeatherData(**data['main'])
