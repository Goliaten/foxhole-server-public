from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Loads environment variables from .env file.
    """

    LOG_LEVEL: str
    FLASK_API_DATETIME_FORMAT: str = "%G-%m-%dT%H:%M:%S%:z"


settings = Settings()  # type: ignore
