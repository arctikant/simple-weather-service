from typing import Annotated

from fastapi import APIRouter, HTTPException, Query

from app.deps import WeatherService
from app.exceptions import WeatherServiceError
from app.schemas.api import Response
from app.schemas.weather import WeatherData, WeatherRequest

router = APIRouter()


@router.get('/weather', response_model=Response[WeatherData])
async def index(query: Annotated[WeatherRequest, Query()], weather: WeatherService) -> Response[WeatherData]:
    try:
        return Response(data=await weather.get_weather(query.city))
    except WeatherServiceError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
