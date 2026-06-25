from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from keyboards.menu import main_menu_keyboard

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await message.answer("Выбери действие:", reply_markup=main_menu_keyboard())


@router.message(Command("help"))
async def cmd_help(message: Message) -> None:
    await message.answer(
        "Доступные кнопки:\n"
        "🌤 Сейчас — текущая погода\n"
        "🕒 По часам — прогноз на 24 часа\n"
        "☀️ Сегодня — прогноз на сегодня\n"
        "🌙 Завтра — прогноз на завтра\n"
        "📅 Неделя — прогноз на 7 дней\n"
        "📊 Модели — сравнение моделей и консенсус",
        reply_markup=main_menu_keyboard(),
    )


@router.message()
async def show_menu(message: Message) -> None:
    await message.answer("Выбери действие:", reply_markup=main_menu_keyboard())
