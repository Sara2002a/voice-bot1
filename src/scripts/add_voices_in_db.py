import re
from os import listdir
from os.path import isdir, isfile, join

from loguru import logger
from sqlalchemy import create_engine
from telegram.ext import ExtBot

from models import available_categories, categories, category_model, voice_model
from settings import settings

voices_assets = "/bot/assets"

bot = ExtBot(token=settings.telegram_token)


def voice_is_valid(file_name: str) -> bool:
    return True if re.match("^.*\S-\S.*.opus$", file_name) else False


def get_voices_from_dir(voices_dir: str) -> list:
    return [f for f in listdir(voices_dir) if isfile(join(voices_dir, f)) and f.endswith("opus")]


def add_voices(category: str) -> None:
    engine, category_dir = create_engine(settings.db_url), join(voices_assets, category)
    dirs = [f for f in listdir(category_dir) if isdir(join(category_dir, f))]
    for voices_dir in dirs:
        category_title, voices_dir = voices_dir, join(category_dir, voices_dir)
        with engine.begin() as connection:
            voices = get_voices_from_dir(voices_dir)
            category_resource = connection.execute(
                category_model.insert().values(title=category_title, category=category)
            )
            for voice in voices:
                if not voice_is_valid(file_name=voice):
                    raise ValueError(f"Voice {voice} not valid.")
                response = bot.send_voice(
                    chat_id=settings.voice_chat, voice=open(join(voices_dir, voice), "rb")
                )
                connection.execute(
                    voice_model.insert().values(
                        telegram_file_id=response.voice.file_id,
                        title=voice.split("-")[1].replace(".opus", ""),
                        performer=voice.split("-")[0],
                        link=response.link,
                        category_uuid=category_resource.inserted_primary_key[0],
                    )
                )
                logger.info(response)


if __name__ == "__main__":
    categories = [f for f in listdir(voices_assets) if isdir(join(voices_assets, f))]
    for category in categories:
        add_voices(category=category)
