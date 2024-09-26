from datetime import UTC, datetime, timedelta

from app.repositories.base import BaseRepository
from app.schemas.weather import WeatherEvent


class WeatherEventRepository(BaseRepository):
    def _get_table_name(self):
        return 'weather_event'

    async def init(self) -> None:
        await self._dynamodb_service.create_table(
            name=self._get_table_name(),
            attribute_definitions=[
                {'AttributeName': 'city', 'AttributeType': 'S'},
                {'AttributeName': 'timestamp', 'AttributeType': 'S'},
            ],
            key_schema=[
                {'AttributeName': 'city', 'KeyType': 'HASH'},
                {'AttributeName': 'timestamp', 'KeyType': 'RANGE'},
            ],
            provisioned_throughput={'ReadCapacityUnits': 1, 'WriteCapacityUnits': 1},
        )

    async def get_last_for_period(self, city: str, seconds=300) -> WeatherEvent | None:
        timestamp = datetime.now(UTC) - timedelta(seconds=seconds)

        response = await self._dynamodb_service.query(
            table=self._get_table_name(),
            expression='city = :city_val AND #ts >= :timestamp_val',
            names={'#ts': 'timestamp'},
            values={
                ':city_val': {'S': city},
                ':timestamp_val': {'S': timestamp.isoformat(timespec='milliseconds')},
            },
            limit=1,
            scan_forward=False,
        )

        if response:
            return WeatherEvent(
                city=response[0]['city']['S'],
                timestamp=datetime.fromisoformat(response[0]['timestamp']['S']),
                s3_url=response[0]['s3_url']['S'],
            )
        else:
            return None

    async def put(self, item: WeatherEvent) -> None:
        await self._dynamodb_service.put(
            table=self._get_table_name(),
            item={
                'city': {'S': item.city},
                'timestamp': {'S': item.timestamp.isoformat(timespec='milliseconds')},
                's3_url': {'S': item.s3_url},
            },
        )


weather_event_repository = WeatherEventRepository()
