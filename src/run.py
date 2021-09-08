#!/usr/bin/sudo python

from loguru import logger

from bot import app
from settings import configure_logger

configure_logger()

logger.info("Run bot...")
app.start_polling()
app.idle()
