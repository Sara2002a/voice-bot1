from pathlib import Path

from pydantic import BaseSettings, Field, PostgresDsn, validator
from sqlalchemy import create_engine

development_mode, production_mode = "development", "production"


class BaseConfig(BaseSettings):
    mode: str = Field(default="production")
    telegram_token: str
    telegram_base_url: str | None
    db_url: PostgresDsn
    voice_chat: str

    @validator("mode")
    def mode_validator(cls, value):
        if value not in (development_mode, production_mode):
            raise ValueError("mode must be production or development")
        return value


base_conf = BaseConfig()
root_dir = Path(__file__).resolve().parent.parent

if base_conf.mode == development_mode:
    from settings.development import settings
else:
    from settings.production import settings

del base_conf

database = create_engine(settings.db_url)
