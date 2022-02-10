from telegram import InlineQueryResultAudio, Update
from telegram.ext import CallbackContext

from bot.utils import check_user
from models import voice_model
from settings import database


@check_user
def search(update: Update, context: CallbackContext) -> None:
    offset = 0 if not update.inline_query.offset else int(update.inline_query.offset)
    update.inline_query.answer(
        [
            InlineQueryResultAudio(
                id=row["uuid"],
                title=row["title"],
                audio_url=row["link"],
                performer=row["performer"],
            )
            for row in database.execute(voice_model.select().limit(50).offset(offset * 50))
        ],
        timeout=10,
        next_offset=offset + 1,
    )


__all__ = ["search"]
