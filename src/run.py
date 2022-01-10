from loguru import logger
from telegram.error import InvalidToken, NetworkError, Unauthorized

from bot import app
from settings import configure_logger

if __name__ == "__main__":
    configure_logger()
    try:
        logger.info("Run bot...")
        app.start_polling()
        app.idle()
    except (InvalidToken, Unauthorized) as err:
        logger.error("Invalid telegram token.")
    except NetworkError as err:
        logger.error("Failed to establish a connection to the server.")
