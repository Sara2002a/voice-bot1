from pydantic import AnyHttpUrl

from settings.base import BaseConfig


class Config(BaseConfig):
    debug: bool
    host: AnyHttpUrl | None


settings = Config(debug=False)
__all__ = ["settings"]
