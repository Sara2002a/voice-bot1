from dataclasses import dataclass


@dataclass
class message_text:
    select_category = "Выберите категорию!"
    voices_not_found = (
        "К сожалению, для данной категории нет голосовых сообщений. "
        "Используйте команду /start для выхода в меню или обратитесь в поддержку!"
    )
    voice_saved = 'Аудиозапись "{}" добавлена в вашу колекцию!'
    voice_already_saved = 'Аудиозапись "{}" уже добавлена!'


@dataclass
class callback_text:
    menu = "Меню"
    back = "Назад"
