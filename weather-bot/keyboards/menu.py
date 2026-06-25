from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def main_menu_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🌤 Сейчас")],
            [KeyboardButton(text="🕒 По часам")],
            [KeyboardButton(text="☀️ Сегодня")],
            [KeyboardButton(text="🌙 Завтра")],
            [KeyboardButton(text="📅 Неделя")],
            [KeyboardButton(text="📊 Модели")],
        ],
        resize_keyboard=True,
    )
