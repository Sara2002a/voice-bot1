from dataclasses import dataclass


@dataclass
class message_text:
    select_category = "Выберите категорию."
    voices_not_found = (
        "К сожалению, для данной категории нет голосовых сообщений. "
        "Используйте команду /start для выхода в меню или обратитесь в поддержку!"
    )


@dataclass
class callback_text:
    menu = "Меню"
    back = "Назад"
