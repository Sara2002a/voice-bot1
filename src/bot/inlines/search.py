from urllib.parse import quote

from sqlalchemy import or_
from telegram import InlineQueryResultAudio, Update, constants
from telegram.ext import CallbackContext

from bot.utils import check_user
from models import user_voice_model, voice_model
from settings import database, settings


@check_user
def search(update: Update, context: CallbackContext) -> None:
    offset = 0 if not update.inline_query.offset else int(update.inline_query.offset)
    voices = (
        voice_model.select()
        .limit(constants.MAX_INLINE_QUERY_RESULTS)
        .offset(offset * constants.MAX_INLINE_QUERY_RESULTS)
        .order_by(user_voice_model.c.created_at)
        .join(user_voice_model, voice_model.c.uuid == user_voice_model.c.voice_uuid, isouter=True)
    )

    if text_search := update.inline_query.query:
        voices = voices.where(
            or_(
                voice_model.c.title.ilike(f"%{text_search}%"),
                voice_model.c.performer.ilike(f"%{text_search}%"),
            )
        )

    update.inline_query.answer(
        [
            InlineQueryResultAudio(
                id=voice["uuid"],
                title=voice["title"],
                audio_url=f"{settings.voice_url}/{settings.telegram_token}/assets/{quote(voice['path'])}",
                performer=voice["performer"],
            )
            for voice in database.execute(voices)
        ],
        cache_time=100,
        is_personal=True,
        timeout=10,
        next_offset=offset + 1,
    )


__all__ = ["search"]
