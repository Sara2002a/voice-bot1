from copy import deepcopy

from sqlalchemy import VARCHAR, Column, ForeignKey, Table, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID

from models.base import base_fields, metadata
from models.utils import initialize_datetime_triggers

voice_model = Table(
    "voices",
    metadata,
    *deepcopy(base_fields),
    # fmt: off
    # more information on the maximum file name and url sizes can be found here:
    # https://serverfault.com/questions/9546/filename-length-limits-on-linux
    # https://stackoverflow.com/questions/417142/what-is-the-maximum-length-of-a-url-in-different-browsers
    Column("title", VARCHAR(length=255), nullable=False, comment="Title"),
    Column("performer", VARCHAR(length=255), nullable=False, comment="Performer"),
    Column("link", VARCHAR(length=2000), nullable=False, unique=True, comment="Link"),
    Column("telegram_file_id", VARCHAR(length=1000), nullable=False, unique=True, comment="Telegram File ID"),
    Column("category_uuid", UUID, ForeignKey("public.categories.uuid", onupdate="CASCADE"), nullable=False, comment="Category UUID"),
    UniqueConstraint("title", "performer", name="voice_constraint"),
    schema="public",
    comment="Voices"
)


create_datetime_trigger, drop_datetime_trigger = initialize_datetime_triggers(model=voice_model)

__all__ = ["voice_model"]
