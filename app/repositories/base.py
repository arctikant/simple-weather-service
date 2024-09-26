from abc import ABC, abstractmethod

from app.core.aws.dynamodb import DynamoDBService


class BaseRepository(ABC):
    def __init__(self) -> None:
        self._dynamodb_service = DynamoDBService()

    @abstractmethod
    def _get_table_name(self):
        raise NotImplementedError
