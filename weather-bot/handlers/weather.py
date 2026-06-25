from aiogram import Router
from aiogram.types import Message

from services.consensus import weighted_consensus
from services.openmeteo import fetch_forecast, fetch_model_temps

router = Router()


@router.message(lambda m: m.text == "🕒 По часам")
async def hourly(message: Message) -> None:
    try:
        data = fetch_forecast()
        temps = data["hourly"]["temperature_2m"][:24]
        times = data["hourly"]["time"][:24]
    except Exception as exc:
        await message.answer(f"Не удалось получить прогноз: {exc}")
        return

    text = "🕒 Почасовой прогноз\n\n"
    for time, temp in zip(times, temps):
        hour = time[11:16]
        text += f"{hour}  {temp:.1f}°\n"

    await message.answer(text)


@router.message(lambda m: m.text == "🌤 Сейчас")
async def now(message: Message) -> None:
    try:
        data = fetch_forecast()
        temp = data["hourly"]["temperature_2m"][0]
        wind = data["hourly"]["wind_speed_10m"][0]
    except Exception as exc:
        await message.answer(f"Не удалось получить погоду: {exc}")
        return

    await message.answer(
        f"🌤 Сейчас\n\n"
        f"Температура: {temp:.1f}°\n"
        f"Ветер: {wind} м/с"
    )


@router.message(lambda m: m.text == "☔ Дождь")
async def rain(message: Message) -> None:
    try:
        data = fetch_forecast()
        probs = data["hourly"]["precipitation_probability"][:24]
        times = data["hourly"]["time"][:24]
    except Exception as exc:
        await message.answer(f"Не удалось получить прогноз осадков: {exc}")
        return

    text = "☔ Вероятность осадков\n\n"
    for time, prob in zip(times, probs):
        hour = time[11:16]
        text += f"{hour}  {prob}%\n"

    await message.answer(text)


@router.message(lambda m: m.text == "📊 Модели")
async def models(message: Message) -> None:
    try:
        temps = fetch_model_temps()
        consensus = weighted_consensus(temps)
    except Exception as exc:
        await message.answer(f"Не удалось получить данные моделей: {exc}")
        return

    text = "📊 Сравнение моделей\n\n"
    for model, temp in temps.items():
        text += f"{model.upper()}: {temp:.1f}°\n"
    text += f"\nКонсенсус: {consensus:.1f}°"

    await message.answer(text)
