from pathlib import Path

from pydantic import BaseSettings, Field, PostgresDsn, validator


class BaseConfig(BaseSettings):
    mode: str = Field(default="production")
    telegram_token: str
    telegram_base_url: str = Field(default="")
    db_url: PostgresDsn
    voice_chat: str

    @validator("mode")
    def mode_validator(cls, value):
        if value not in ["production", "development"]:
            raise ValueError("mode must be production or development")
        return value


base_conf = BaseConfig()
root_dir = Path(__file__).resolve().parent.parent

if base_conf.mode == "dev":
    from settings.development import settings
else:
    from settings.production import settings

del base_conf
