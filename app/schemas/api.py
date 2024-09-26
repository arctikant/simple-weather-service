from enum import Enum
from typing import Any, Generic, TypeVar

from pydantic import BaseModel


class ResponseStatus(Enum):
    SUCCESS: int = 0
    ERROR: int = 100


T = TypeVar('T')


class Response(BaseModel, Generic[T]):
    code: ResponseStatus = ResponseStatus.SUCCESS
    message: str | None = None
    data: T | None = None

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)
        if self.message is None:
            self.message = self.code.name.lower().replace('_', ' ')
