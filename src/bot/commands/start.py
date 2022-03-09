from sqlalchemy.exc import IntegrityError
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.error import BadRequest
from telegram.ext import CallbackContext

from bot.utils import check_user, mt
from models import category_model, user_model
from settings import database


@check_user
def start(update: Update, context: CallbackContext) -> None:
    try:
        database.execute(user_model.insert().values(telegram_id=update.effective_user.id))
    except IntegrityError:
        pass

    reply_markup = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(row["title"], callback_data=row["slug"].value)]
            for row in database.execute(category_model.select())
        ]
    )
    for voices_message_id in context.user_data.get("voices_message_id", []):
        try:
            context.bot.delete_message(
                chat_id=update.effective_chat.id, message_id=voices_message_id
            )
        except BadRequest:
            pass

    _start_answer(update=update, text=mt.select_category, reply_markup=reply_markup)
    context.user_data["voices_message_id"] = []


def _start_answer(update: Update, text: str, reply_markup=None) -> None:
    if update.message:
        update.message.reply_text(text, reply_markup=reply_markup)
    elif update.callback_query.message.text:
        update.callback_query.message.edit_text(text, reply_markup=reply_markup)
    else:
        update.callback_query.message.reply_text(text, reply_markup=reply_markup)


__all__ = ["start"]
