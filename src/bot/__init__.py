from telegram.ext import CommandHandler, InlineQueryHandler, Updater

from bot.commands.start import start
from bot.inlines.search import search
from settings import settings

if settings.telegram_base_url:
    app = Updater(token=settings.telegram_token, base_url=settings.telegram_base_url)
else:
    app = Updater(token=settings.telegram_token)

# commands
app.dispatcher.add_handler(CommandHandler("start", start, run_async=True))

# lnlines
app.dispatcher.add_handler(InlineQueryHandler(search))
