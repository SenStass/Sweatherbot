from aiogram import Router
from aiogram.types import Message

from services.consensus import weighted_consensus
from services.display import (
    format_current_weather,
    format_day_forecast,
    format_hourly_forecast,
    format_weekly_forecast,
)
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
        apparent_temperature = data["hourly"]["apparent_temperature"][:24]
        humidity = data["hourly"]["relative_humidity_2m"][:24]
        wind_speed = data["hourly"]["wind_speed_10m"][:24]
    except Exception as exc:
        await message.answer(f"Не удалось получить прогноз: {exc}")
        return

    text = format_hourly_forecast(
        times=times,
        temps=temps,
        cloud_cover=cloud_cover,
        precipitation_probability=precipitation_probability,
        is_day=is_day,
        apparent_temperature=apparent_temperature,
        humidity=humidity,
        wind_speed=wind_speed,
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
        weather_code = data["hourly"].get("weather_code", [None])[0]
        wind_direction = data["hourly"].get("wind_direction_10m", [None])[0]
        local_time = data.get("current_weather", {}).get("time")
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
        weather_code=weather_code,
        wind_direction=wind_direction,
        local_time=local_time,
    )

    await message.answer(text)


@router.message(lambda m: m.text == "☀️ Сегодня")
async def today(message: Message) -> None:
    try:
        data = fetch_forecast()
        daily = data["daily"]
        text = format_day_forecast(
            title="☀️ Сегодня",
            date=daily["time"][0],
            max_temp=daily["temperature_2m_max"][0],
            min_temp=daily["temperature_2m_min"][0],
            precipitation_probability=daily["precipitation_probability_mean"][0],
            cloud_cover=daily["cloud_cover_mean"][0],
            weather_code=daily.get("weather_code", [None])[0],
        )
    except Exception as exc:
        await message.answer(f"Не удалось получить прогноз на сегодня: {exc}")
        return

    await message.answer(text)


@router.message(lambda m: m.text == "🌙 Завтра")
async def tomorrow(message: Message) -> None:
    try:
        data = fetch_forecast()
        daily = data["daily"]
        text = format_day_forecast(
            title="🌙 Завтра",
            date=daily["time"][1],
            max_temp=daily["temperature_2m_max"][1],
            min_temp=daily["temperature_2m_min"][1],
            precipitation_probability=daily["precipitation_probability_mean"][1],
            cloud_cover=daily["cloud_cover_mean"][1],
            weather_code=daily.get("weather_code", [None])[1],
        )
    except Exception as exc:
        await message.answer(f"Не удалось получить прогноз на завтра: {exc}")
        return

    await message.answer(text)


@router.message(lambda m: m.text == "📅 Неделя")
async def weekly(message: Message) -> None:
    try:
        data = fetch_forecast()
        dates = data["daily"]["time"][:7]
        max_temps = data["daily"]["temperature_2m_max"][:7]
        min_temps = data["daily"]["temperature_2m_min"][:7]
        precipitation_probability = data["daily"]["precipitation_probability_mean"][:7]
        cloud_cover = data["daily"]["cloud_cover_mean"][:7]
    except Exception as exc:
        await message.answer(f"Не удалось получить недельный прогноз: {exc}")
        return

    text = format_weekly_forecast(
        dates=dates,
        max_temps=max_temps,
        min_temps=min_temps,
        precipitation_probability=precipitation_probability,
        cloud_cover=cloud_cover,
    )

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
