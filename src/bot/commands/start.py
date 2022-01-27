from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext

from bot.utils import callback_text as ct
from bot.utils import check_user
from bot.utils import message_text as mt


@check_user
def start(update: Update, context: CallbackContext) -> None:
    reply_markup = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(mt.games.value, callback_data=ct.games.value)],
            [InlineKeyboardButton(mt.films.value, callback_data=ct.films.value)],
        ]
    )
    update.message.reply_text("Выберите категорию", reply_markup=reply_markup)


__all__ = ["start"]
