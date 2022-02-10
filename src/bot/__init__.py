from telegram.ext import CallbackQueryHandler, CommandHandler, InlineQueryHandler, Updater

from bot.callbacks.voices import show_voices
from bot.commands.start import start
from bot.inlines.search import search
from settings import settings

if settings.telegram_base_url:
    app = Updater(token=settings.telegram_token, base_url=settings.telegram_base_url)
else:
    app = Updater(token=settings.telegram_token)

# callbacks
app.dispatcher.add_handler(CallbackQueryHandler(start, pattern="show_menu", run_async=True))
app.dispatcher.add_handler(CallbackQueryHandler(show_voices, pattern="", run_async=True))

# commands
app.dispatcher.add_handler(CommandHandler("start", start, run_async=True))

# lnlines
app.dispatcher.add_handler(InlineQueryHandler(search))
