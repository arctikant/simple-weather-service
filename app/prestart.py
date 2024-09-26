import asyncio

from app.core.logging import logger
from app.repositories.weather_event import weather_event_repository
from app.storages.weather import weather_storage


async def init_s3() -> None:
    logger.info('Initializing S3')
    await weather_storage.init()


async def init_dynamodb() -> None:
    logger.info('Initializing DynamoDB')
    await weather_event_repository.init()


async def main() -> None:
    await init_s3()
    await init_dynamodb()


if __name__ == '__main__':
    asyncio.run(main())
