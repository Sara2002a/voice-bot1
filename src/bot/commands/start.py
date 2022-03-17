from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.error import BadRequest
from telegram.ext import CallbackContext

from bot.utils import check_user, mt
from bot.utils.decorators import delete_previous_messages
from models import category_model
from settings import database


@check_user
@delete_previous_messages
def start(update: Update, context: CallbackContext) -> None:
    reply_markup = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(row["title"], callback_data=row["slug"].value)]
            for row in database.execute(category_model.select())
        ]
    )
    _start_answer(update=update, text=mt.select_category, reply_markup=reply_markup)


def _start_answer(update: Update, text: str, reply_markup=None) -> None:
    if update.message:
        update.message.reply_text(text, reply_markup=reply_markup)
    else:
        update.callback_query.message.reply_text(text, reply_markup=reply_markup)


__all__ = ["start"]
