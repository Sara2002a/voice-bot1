from loguru import logger
from sqlalchemy import create_engine
from telegram import InlineQueryResultAudio, Update
from telegram.ext import CallbackContext

from bot.utils import check_user
from models import voice_model
from settings import settings


@check_user
def search(update: Update, context: CallbackContext) -> None:
    engine = create_engine(settings.db_url)
    with engine.connect() as connection:
        answer = [
            InlineQueryResultAudio(
                id=row["uuid"],
                title=row["title"],
                audio_url=row["link"],
                performer=row["performer"],
            )
            for row in connection.execute(voice_model.select())
        ]

    update.inline_query.answer(answer)


__all__ = ["search"]
