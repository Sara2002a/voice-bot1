from telegram import Update
from telegram.ext import CallbackContext

from bot.utils import check_user


@check_user
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Hello!")
