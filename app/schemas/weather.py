from datetime import datetime

from pydantic import BaseModel, Field


class WeatherRequest(BaseModel):
    city: str | None = Field(min_length=3, max_length=50)


class WeatherData(BaseModel):
    temp: float
    feels_like: float
    temp_min: float
    temp_max: float
    pressure: int
    humidity: int
    sea_level: int
    grnd_level: int


class WeatherEvent(BaseModel):
    city: str = Field(min_length=3, max_length=50)
    timestamp: datetime
    s3_url: str
