from datetime import datetime
from typing import Optional


def _cloud_icon(cloud_cover: int) -> str:
    if cloud_cover >= 70:
        return "☁️"
    if cloud_cover >= 40:
        return "⛅"
    if cloud_cover >= 20:
        return "🌤️"
    return "☀️"


def _precipitation_icon(probability: int, weather_code: Optional[int] = None) -> str:
    if weather_code is not None:
        if weather_code in {95, 96, 99}:
            return "⛈️"
        if weather_code in {71, 73, 75, 77, 85, 86}:
            return "🌨️"
        if weather_code in {45, 48}:
            return "🌫️"

    if probability >= 50:
        return "🌧️"
    if probability >= 20:
        return "🌦"
    return "☀️"


def _day_icon(is_day: int) -> str:
    return "☀️" if is_day else "🌙"


def _wind_icon(wind_direction: Optional[int]) -> str:
    if wind_direction is None:
        return "💨"

    sectors = [
        (348.75, 360, "⬆️"),
        (0, 11.25, "⬆️"),
        (11.25, 33.75, "↗️"),
        (33.75, 56.25, "↗️"),
        (56.25, 78.75, "➡️"),
        (78.75, 101.25, "➡️"),
        (101.25, 123.75, "↘️"),
        (123.75, 146.25, "↘️"),
        (146.25, 168.75, "⬇️"),
        (168.75, 191.25, "⬇️"),
        (191.25, 213.75, "↙️"),
        (213.75, 236.25, "↙️"),
        (236.25, 258.75, "⬅️"),
        (258.75, 281.25, "⬅️"),
        (281.25, 303.75, "↖️"),
        (303.75, 326.25, "↖️"),
        (326.25, 348.75, "⬆️"),
    ]

    for start, end, icon in sectors:
        if start <= wind_direction < end:
            return icon

    return "💨"


def _temperature_color(temp: float) -> str:
    if temp < 0:
        return "🔵"
    if temp < 15:
        return "🟢"
    if temp < 25:
        return "🟡"
    return "🔴"


def _format_time(value: str) -> str:
    if not value:
        return "-"

    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return parsed.strftime("%H:%M")
    except ValueError:
        return value


def _format_datetime(value: str) -> str:
    if not value:
        return "-"

    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return parsed.strftime("%H:%M:%S %d.%m.%Y")
    except ValueError:
        return value


def format_current_weather(
    temp: float,
    wind: float,
    cloud_cover: int,
    precipitation_probability: int,
    is_day: int,
    sunrise: str,
    sunset: str,
    weather_code: Optional[int] = None,
    wind_direction: Optional[int] = None,
    local_time: Optional[str] = None,
) -> str:
    cloud_icon = _cloud_icon(cloud_cover)
    rain_icon = _precipitation_icon(precipitation_probability, weather_code)
    day_icon = _day_icon(is_day)
    sunrise_text = _format_datetime(sunrise)
    sunset_text = _format_datetime(sunset)
    wind_icon = _wind_icon(wind_direction)
    temp_color = _temperature_color(temp)
    local_time_text = _format_time(local_time) if local_time else "-"

    return (
        f"🌤 Сейчас\n\n"
        f"{day_icon} Температура: {temp_color} {temp:.1f}°\n"
        f"{cloud_icon} Облачность: {cloud_cover}%\n"
        f"{rain_icon} Дождь: {precipitation_probability}%\n"
        f"{wind_icon} Ветер: {wind:.1f} м/с"
        f"  {wind_direction}°\n"
        f"🕒 Локальное время: {local_time_text}\n"
        f"🌅 Восход: {sunrise_text}\n"
        f"🌇 Закат: {sunset_text}"
    )


def format_hourly_forecast(
    times: list[str],
    temps: list[float],
    cloud_cover: list[int],
    precipitation_probability: list[int],
    is_day: list[int],
    apparent_temperature: list[float],
    humidity: list[int],
    wind_speed: list[float],
) -> str:
    lines = ["🕒 Почасовой прогноз", ""]
    header = "Время | Темп. | Ощущ. | Осадки | Ветер | Влажн. | Облачн."
    lines.append(header)

    for time, temp, cloud, rain, day, feels_like, humidity_value, wind_value in zip(
        times,
        temps,
        cloud_cover,
        precipitation_probability,
        is_day,
        apparent_temperature,
        humidity,
        wind_speed,
    ):
        hour = time[11:16]
        day_icon = _day_icon(day)
        cloud_icon = _cloud_icon(cloud)
        rain_icon = _precipitation_icon(rain)
        line = (
            f"{hour} | {day_icon} {temp:+.0f}° | {feels_like:+.0f}° | "
            f"{rain_icon} {rain:>3}% | {wind_value:>4.0f} м/с | {humidity_value:>3}% | {cloud_icon} {cloud:>3}%"
        )
        lines.append(line)

    return "\n".join(lines)


def format_day_forecast(
    title: str,
    date: str,
    max_temp: float,
    min_temp: float,
    precipitation_probability: int,
    cloud_cover: int,
    weather_code: Optional[int] = None,
) -> str:
    date_text = datetime.fromisoformat(date).strftime("%d.%m")
    cloud_icon = _cloud_icon(cloud_cover)
    rain_icon = _precipitation_icon(precipitation_probability, weather_code)
    temp_color = _temperature_color(max_temp)

    return (
        f"{title}\n\n"
        f"📅 {date_text}\n"
        f"{temp_color} Макс: {max_temp:.1f}°  Мин: {min_temp:.1f}°\n"
        f"{cloud_icon} Облачность: {cloud_cover}%\n"
        f"{rain_icon} Осадки: {precipitation_probability}%"
    )


def format_weekly_forecast(
    dates: list[str],
    max_temps: list[float],
    min_temps: list[float],
    precipitation_probability: list[int],
    cloud_cover: list[int],
) -> str:
    lines = ["📅 Прогноз на 7 дней\n"]

    for date, max_temp, min_temp, rain, cloud in zip(
        dates,
        max_temps,
        min_temps,
        precipitation_probability,
        cloud_cover,
    ):
        date_text = datetime.fromisoformat(date).strftime("%d.%m")
        cloud_icon = _cloud_icon(cloud)
        rain_icon = _precipitation_icon(rain)
        temp_color = _temperature_color(max_temp)
        lines.append(
            f"{date_text}  {temp_color} {max_temp:.1f}°/{min_temp:.1f}°  {cloud_icon} {cloud}%  {rain_icon} {rain}%"
        )

    return "\n".join(lines)
