import math

from sqlalchemy import func, select
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.error import BadRequest
from telegram.ext import CallbackContext

from bot.utils import check_user, ct, mt
from models import available_categories, category_model, subcategory_model, voice_model
from settings import database

MAX_PAGES, MAX_VOICES = 5, 5


@check_user
def show_voices(update: Update, context: CallbackContext) -> None:
    callback_data = update.callback_query.data

    if callback_data.endswith("*"):
        return

    if callback_data in [e.value for e in available_categories]:
        _show_categories(update=update, context=context, data=callback_data)
        return

    _show_voices(update=update, context=context, data=callback_data)


def _show_categories(update: Update, context: CallbackContext, data: str) -> None:
    subcategories = (
        voice_model.select()
        .distinct()
        .select_from(voice_model)
        .with_only_columns(subcategory_model.c.title, subcategory_model.c.slug)
        .where(category_model.c.slug == data)
        .join(category_model, voice_model.c.category_uuid == category_model.c.uuid)
        .join(subcategory_model, voice_model.c.subcategory_uuid == subcategory_model.c.uuid)
    )

    keyboard = [
        [InlineKeyboardButton(row["title"], callback_data=f"{data}_{row['slug']}_1")]
        for row in database.execute(subcategories)
    ]
    keyboard.append([InlineKeyboardButton(ct.back, callback_data="show_menu")])

    update.callback_query.message.edit_text(
        mt.select_category if len(keyboard) > 1 else mt.voices_not_found,
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


def _show_voices(update: Update, context: CallbackContext, data: str) -> None:
    category, subcategory, page = data.split("_")
    current_page = int(page)

    count_voices = database.execute(
        select(func.count("*"))
        .select_from(voice_model)
        .where(category_model.c.slug == category)
        .where(subcategory_model.c.slug == subcategory)
        .join(category_model, voice_model.c.category_uuid == category_model.c.uuid)
        .join(subcategory_model, voice_model.c.subcategory_uuid == subcategory_model.c.uuid)
    ).scalar()

    voices_query = (
        voice_model.select()
        .with_only_columns(voice_model.c.telegram_file_id)
        .where(category_model.c.slug == category)
        .where(subcategory_model.c.slug == subcategory)
        .limit(MAX_VOICES)
        .offset((MAX_PAGES * current_page) - MAX_PAGES)
        .join(category_model, voice_model.c.category_uuid == category_model.c.uuid)
        .join(subcategory_model, voice_model.c.subcategory_uuid == subcategory_model.c.uuid)
    )

    real_count_pages, pages_buttons = math.ceil(count_voices / MAX_VOICES), []
    start_page, end_page = _get_pages_info(
        current_page=current_page, real_count_pages=real_count_pages
    )

    if current_page + 2 > MAX_PAGES:
        pages_buttons.append(
            InlineKeyboardButton("<", callback_data=f"{category}_{subcategory}_{current_page - 1}")
        )

    for page_idx in range(start_page, end_page + 1):
        if current_page == page_idx:
            page_idx = "*"
        pages_buttons.append(
            InlineKeyboardButton(
                f"{page_idx}", callback_data=f"{category}_{subcategory}_{page_idx}"
            )
        )

    if current_page + 2 < real_count_pages and real_count_pages > MAX_PAGES:
        pages_buttons.append(
            InlineKeyboardButton(">", callback_data=f"{category}_{subcategory}_{current_page + 1}")
        )

    if voices := database.execute(voices_query):
        reply_markup = InlineKeyboardMarkup(
            [
                pages_buttons,
                [
                    InlineKeyboardButton(ct.menu, callback_data="show_menu"),
                ],
            ]
        )
        update.callback_query.message.delete()
        for voices_message_id in context.user_data.get("voices_message_id", []):
            try:
                res = context.bot.delete_message(
                    chat_id=update.effective_chat.id, message_id=voices_message_id
                )
            except BadRequest:
                pass

        voices_message_id = []
        for index, voice in enumerate(voices, start=1):
            if index == voices.rowcount:
                res = update.callback_query.message.reply_voice(
                    voice["telegram_file_id"], reply_markup=reply_markup
                )
            else:
                res = update.callback_query.message.reply_voice(voice["telegram_file_id"])

            voices_message_id.append(res.message_id)
        context.user_data["voices_message_id"] = voices_message_id


def _get_pages_info(current_page: int, real_count_pages: int) -> tuple:
    if real_count_pages <= MAX_PAGES:
        return 1, real_count_pages
    else:
        if current_page in [1, 2]:
            return 1, MAX_PAGES if real_count_pages > MAX_PAGES else real_count_pages
        elif current_page + 2 < real_count_pages:
            return current_page - 2, current_page + 2
        else:
            return real_count_pages - (MAX_PAGES - 1), real_count_pages


__all__ = ["show_voices"]
