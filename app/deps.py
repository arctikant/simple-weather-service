from typing import Annotated

from fastapi import Depends

from app.services.weather import WeatherService as WeatherServiceClass


async def get_weather_service() -> WeatherServiceClass:
    return WeatherServiceClass()


WeatherService = Annotated[WeatherServiceClass, Depends(get_weather_service)]
