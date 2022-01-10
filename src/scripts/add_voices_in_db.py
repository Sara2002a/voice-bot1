from os import listdir
from os.path import isfile, join

from loguru import logger
from sqlalchemy import create_engine
from telegram.ext import ExtBot

from models.voices import voice_model
from settings import settings

voices_dir = "/bot/assets"

bot = ExtBot(token=settings.telegram_token)


def add_voices():
    engine = create_engine(settings.db_url)
    voice_files = [
        f for f in listdir(voices_dir) if isfile(join(voices_dir, f)) and f.endswith("opus")
    ]
    for voice in voice_files:
        response = bot.send_voice(
            chat_id=settings.voice_chat, voice=open(join(voices_dir, voice), "rb")
        )
        with engine.begin() as connection:
            connection.execute(
                voice_model.insert().values(
                    title=voice.split("-")[1].replace(".opus", ""),
                    performer=voice.split("-")[0],
                    link=response.link,
                )
            )
        logger.error(response)


if __name__ == "__main__":
    add_voices()
