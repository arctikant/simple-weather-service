from cerberus import Validator
from fastapi import status
from httpx import AsyncClient

from app.core.config import settings
from app.schemas.api import ResponseStatus


class TestWeatherRouter:
    async def test_user_can_get_weather_for_existing_city(self, client: AsyncClient) -> None:
        response = await client.get(
            f'{settings.API_V1_STR}/weather',
            params={'city': 'London'},
        )
        body = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert body['code'] == ResponseStatus.SUCCESS.value

        schema = {
            'code': {'type': 'integer'},
            'message': {'type': 'string'},
            'data': {
                'type': 'dict',
                'schema': {
                    'temp': {'type': 'float'},
                    'feels_like': {'type': 'float'},
                    'temp_min': {'type': 'float'},
                    'temp_max': {'type': 'float'},
                    'pressure': {'type': 'integer'},
                    'humidity': {'type': 'integer'},
                    'sea_level': {'type': 'integer'},
                    'grnd_level': {'type': 'integer'},
                },
            },
        }

        assert Validator(schema).validate(body)

    async def test_user_can_get_error_for_non_existing_city(self, client: AsyncClient) -> None:
        response = await client.get(
            f'{settings.API_V1_STR}/weather',
            params={'city': 'non-existing'},
        )

        body = response.json()

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert body['code'] == ResponseStatus.ERROR.value

        schema = {'code': {'type': 'integer'}, 'message': {'type': 'string'}}

        assert Validator(schema).validate(body)
