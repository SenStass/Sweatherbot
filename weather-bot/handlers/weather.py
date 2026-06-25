from aiogram import Router
from aiogram.types import Message

from services.consensus import weighted_consensus
from services.display import format_current_weather, format_hourly_forecast
from services.openmeteo import fetch_forecast, fetch_model_temps

router = Router()


@router.message(lambda m: m.text == "🕒 По часам")
async def hourly(message: Message) -> None:
    try:
        data = fetch_forecast()
        temps = data["hourly"]["temperature_2m"][:24]
        times = data["hourly"]["time"][:24]
        cloud_cover = data["hourly"]["cloud_cover"][:24]
        precipitation_probability = data["hourly"]["precipitation_probability"][:24]
        is_day = data["hourly"]["is_day"][:24]
    except Exception as exc:
        await message.answer(f"Не удалось получить прогноз: {exc}")
        return

    text = format_hourly_forecast(
        times=times,
        temps=temps,
        cloud_cover=cloud_cover,
        precipitation_probability=precipitation_probability,
        is_day=is_day,
    )

    await message.answer(text)


@router.message(lambda m: m.text == "🌤 Сейчас")
async def now(message: Message) -> None:
    try:
        data = fetch_forecast()
        temp = data["hourly"]["temperature_2m"][0]
        wind = data["hourly"]["wind_speed_10m"][0]
        cloud_cover = data["hourly"]["cloud_cover"][0]
        precipitation_probability = data["hourly"]["precipitation_probability"][0]
        is_day = data["hourly"]["is_day"][0]
        sunrise = data["daily"]["sunrise"][0]
        sunset = data["daily"]["sunset"][0]
    except Exception as exc:
        await message.answer(f"Не удалось получить погоду: {exc}")
        return

    text = format_current_weather(
        temp=temp,
        wind=wind,
        cloud_cover=cloud_cover,
        precipitation_probability=precipitation_probability,
        is_day=is_day,
        sunrise=sunrise,
        sunset=sunset,
    )

    await message.answer(text)


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
