import re
from pathlib import Path
from time import sleep

from loguru import logger
from sqlalchemy import Table, create_engine
from sqlalchemy.exc import IntegrityError
from telegram import Message
from telegram.error import RetryAfter
from telegram.ext import ExtBot

from models import category_model, emotion_model, subcategory_model, voice_model
from settings import settings

assets_dir = Path("/bot/assets")

database = create_engine(settings.db_url)

bot = ExtBot(token=settings.telegram_token)


def category_is_valid(file_name: str) -> bool:
    return True if re.match("^.*\S-\S.*$", file_name) else False


def subcategory_is_valid(file_name: str) -> bool:
    return category_is_valid(file_name=file_name)


def voice_is_valid(file_name: str) -> bool:
    return True if re.match("^.*\S-\S.*.opus$", file_name) else False


def get_voices_from_dir(voice_dir: Path) -> list:
    return [voice for voice in voice_dir.iterdir() if voice.is_file()]


def _create_resource(title: str, slug: str, model: Table):
    try:
        return database.execute(
            model.insert().returning(model.c.uuid).values(title=title, slug=slug)
        ).first()
    except IntegrityError:
        return database.execute(
            model.select().with_only_columns(model.c.uuid).where(model.c.slug == slug)
        ).first()


def create_category(category: str):
    title, slug = category.split("-", maxsplit=1)
    return _create_resource(title=title, slug=slug, model=category_model)


def create_subcategory(subcategory: str):
    title, slug = subcategory.split("-", maxsplit=1)
    return _create_resource(title=title, slug=slug, model=subcategory_model)


def create_emotion(title: str):
    emotions = {
        "Обо мне": "me",
        "Радость": "happy",
        "Грусть": "sadness",
        "Злость": "anger",
        "Вопрос": "question",
        "Злорадство": "gloat",
        "Согласие": "agreement",
        "Угроза": "threat",
        "Ревность": "jealousy",
        "Воодушевление": "inspiration",
        "Разочарование": "disappointment",
        "Приказ": "command",
        "Приветствие": "greetings",
        "Ответ": "answer",
        "Сарказм": "sarcasm",
        "Другое": "other",
    }
    if not emotions.get(title):
        return None
    return _create_resource(title=title, slug=emotions.get(title), model=emotion_model)


def add_voice(voice_title: Path, tg_info: Message, category, subcategory, emotion):
    database.execute(
        voice_model.insert().values(
            title=voice_title.name.split("-")[1].replace(".opus", ""),
            performer=voice_title.name.split("-")[0],
            link=tg_info.link,
            telegram_file_id=tg_info.voice.file_id,
            category_uuid=category[0],
            emotion_uuid=emotion[0],
            subcategory_uuid=subcategory[0],
        )
    )


def parse_voices_dir(category: Path) -> None:
    category_resource = create_category(category.name)

    for subcategory in [subcategory for subcategory in category.iterdir() if subcategory.is_dir()]:
        if not subcategory_is_valid(file_name=subcategory.name):
            logger.error(f"Subcategory {voice} not valid.")
            continue

        subcategory_resource = create_subcategory(subcategory.name)

        for emotion in [emotion for emotion in subcategory.iterdir() if emotion.is_dir()]:
            voices = get_voices_from_dir(voice_dir=emotion)

            emotion_resource = create_emotion(emotion.name)

            if emotion_resource is None:
                continue

            for voice in voices:
                if (
                    not voice_is_valid(file_name=voice.name)
                    or database.execute(
                        voice_model.select()
                        .with_only_columns(voice_model.c.uuid)
                        .where(
                            voice_model.c.title == voice.name.split("-")[1].replace(".opus", "")
                        )
                    ).first()
                ):
                    continue

                try:
                    tg_info = bot.send_voice(
                        chat_id=settings.voice_chat, voice=open(emotion / voice, "rb")
                    )
                except RetryAfter as err:
                    logger.error(f"Sleep {err.retry_after + 1.0}")
                    sleep(err.retry_after + 1.0)
                    tg_info = bot.send_voice(
                        chat_id=settings.voice_chat, voice=open(emotion / voice, "rb")
                    )

                try:
                    add_voice(
                        voice_title=voice,
                        tg_info=tg_info,
                        category=category_resource,
                        subcategory=subcategory_resource,
                        emotion=emotion_resource,
                    )
                    logger.info(f"Voice {voice} added.")
                except IntegrityError:
                    pass


if __name__ == "__main__":
    for category in [category for category in assets_dir.iterdir() if category.is_dir()]:
        if not category_is_valid(file_name=category.name):
            logger.error(f"Category {category} is not valid.")
            continue
        parse_voices_dir(category=category)
