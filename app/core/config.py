import warnings
from typing import Annotated, Any, Literal, Self

from pydantic import (
    AnyUrl,
    BeforeValidator,
    computed_field,
    model_validator,
)
from pydantic_settings import BaseSettings, SettingsConfigDict


def parse_cors(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith('['):
        return [i.strip() for i in v.split(',')]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        # Use top level .env file (one level above ./backend/)
        env_file='.env',
        env_ignore_empty=True,
        extra='ignore',
    )

    SECRET_KEY: str
    ENVIRONMENT: Literal['local', 'staging', 'production'] = 'local'
    PROJECT_NAME: str
    DOMAIN: str

    @computed_field  # type: ignore[prop-decorator]
    @property
    def app_url(self) -> str:
        if self.ENVIRONMENT in ['local', 'testing']:
            return f'http://{self.DOMAIN}'
        return f'https://{self.DOMAIN}'

    API_V1_STR: str = '/api/v1'
    BACKEND_CORS_ORIGINS: Annotated[list[AnyUrl] | str, BeforeValidator(parse_cors)] = []
    WEATHER_CACHE_TTL_SECONDS: int

    @computed_field  # type: ignore[prop-decorator]
    @property
    def all_cors_origins(self) -> list[str]:
        return [str(origin).rstrip('/') for origin in self.BACKEND_CORS_ORIGINS]

    def _check_default_secret(self, var_name: str, value: str | None) -> None:
        if value == 'changethis':
            message = (
                f'The value of {var_name} is "changethis", ' 'for security, please change it, at least for deployments.'
            )
            if self.ENVIRONMENT == 'local':
                warnings.warn(message, stacklevel=1)
            else:
                raise ValueError(message)

    @model_validator(mode='after')
    def _enforce_non_default_secrets(self) -> Self:
        self._check_default_secret('SECRET_KEY', self.SECRET_KEY)
        self._check_default_secret('OPEN_WEATHER_API_KEY', self.OPEN_WEATHER_API_KEY)

        return self

    OPEN_WEATHER_API_KEY: str
    OPEN_WEATHER_URL: str

    AWS_ACCESS_KEY_ID: str
    AWS_ACCESS_KEY_SECRET: str
    AWS_REGION_NAME: str
    AWS_ENDPOINT_URL: str


settings = Settings()  # type: ignore
