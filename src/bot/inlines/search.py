from asyncio.log import logger
from operator import or_
from telegram import InlineQueryResultAudio, Update, constants
from telegram.ext import CallbackContext
from sqlalchemy import or_
from bot.utils import check_user
from models import voice_model, voices
from settings import database


@check_user
def search(update: Update, context: CallbackContext) -> None:
    offset = 0 if not update.inline_query.offset else int(update.inline_query.offset)
    voices = (
        voice_model.select()
        .limit(constants.MAX_INLINE_QUERY_RESULTS)
        .offset(offset * constants.MAX_INLINE_QUERY_RESULTS)
    )

    if text_search := update.inline_query.query:
        voices = voices.where(
            or_(
                voice_model.c.title.like(f"%{text_search}%"),
                voice_model.c.performer.like(f"%{text_search}%"),
            )
        )

    update.inline_query.answer(
        [
            InlineQueryResultAudio(
                id=row["uuid"],
                title=row["title"],
                audio_url=row["link"],
                performer=row["performer"],
            )
            for row in database.execute(voices)
        ],
        timeout=10,
        next_offset=offset + 1,
    )


__all__ = ["search"]
