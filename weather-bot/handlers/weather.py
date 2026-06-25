from aiogram import Router
from aiogram.types import Message

from api.meteoinfo import fetch_meteoinfo_forecast
from services.display import format_hourly_forecast

router = Router()


def build_hourly_forecast_payload(items: list[dict[str, object]]) -> dict[str, list[object]]:
    times: list[str] = []
    temps: list[float] = []
    cloud_cover: list[int] = []
    precipitation_probability: list[int] = []
    is_day: list[int] = []
    apparent_temperature: list[float] = []
    humidity: list[int] = []
    wind_speed: list[float] = []

    for item in items[:24]:
        hour = item.get("time")
        if isinstance(hour, str):
            times.append(f"2024-01-01T{hour}")
        else:
            times.append("")

        temps.append(float(item.get("temperature", 0) or 0))
        cloud_cover.append(int(item.get("cloudiness", 0) or 0))
        precipitation_probability.append(min(100, max(0, int(float(item.get("precipitation", 0) or 0) * 10))))
        is_day.append(1)
        apparent_temperature.append(float(item.get("temperature", 0) or 0))
        humidity.append(int(item.get("humidity", 0) or 0))
        wind_speed.append(float(item.get("wind", 0) or 0))

    return {
        "times": times,
        "temps": temps,
        "cloud_cover": cloud_cover,
        "precipitation_probability": precipitation_probability,
        "is_day": is_day,
        "apparent_temperature": apparent_temperature,
        "humidity": humidity,
        "wind_speed": wind_speed,
    }


@router.message(lambda m: m.text == "🕒 По часам")
async def hourly(message: Message) -> None:
    try:
        meteoinfo_items = await fetch_meteoinfo_forecast()
        payload = build_hourly_forecast_payload(meteoinfo_items)
    except Exception as exc:
        await message.answer(f"Не удалось получить прогноз: {exc}")
        return

    text = format_hourly_forecast(
        times=payload["times"],
        temps=payload["temps"],
        cloud_cover=payload["cloud_cover"],
        precipitation_probability=payload["precipitation_probability"],
        is_day=payload["is_day"],
        apparent_temperature=payload["apparent_temperature"],
        humidity=payload["humidity"],
        wind_speed=payload["wind_speed"],
    )

    await message.answer(text)


@router.message(lambda m: m.text in {"🌤 Сейчас", "🌤️ Сейчас"})
async def now(message: Message) -> None:
    await message.answer("Данные о текущей погоде временно недоступны")


@router.message(lambda m: m.text == "☀️ Сегодня")
async def today(message: Message) -> None:
    await message.answer("Данные о прогнозе на сегодня временно недоступны")


@router.message(lambda m: m.text in {"🌙 Завтра", "🌤️ Завтра"})
async def tomorrow(message: Message) -> None:
    await message.answer("Данные о прогнозе на завтра временно недоступны")


@router.message(lambda m: m.text == "📅 Неделя")
async def weekly(message: Message) -> None:
    await message.answer("Данные о недельном прогнозе временно недоступны")


@router.message(lambda m: m.text == "📊 Модели")
async def models(message: Message) -> None:
    await message.answer("Модели временно недоступны")
