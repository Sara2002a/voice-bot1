from loguru import logger
from telegram import Update
from telegram.ext import CallbackContext
from telegram.error import BadRequest, Unauthorized


def start(update: Update, context: CallbackContext):
    try:
        user = update.effective_user
        if user.is_bot:
            logger.warning(
                "Attempt to login from bot with id: {} and name: {}".format(
                    user.bot.id, user.bot.name
                )
            )
            update.message.reply_text("Bots are not allowed!")
            return
        else:
            update.message.reply_text("Hello!")

    except (BadRequest, Unauthorized) as err:
        logger.error("Error: {}\nUser: {}".format(err, update.effective_user.id))
