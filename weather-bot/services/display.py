def _cloud_icon(cloud_cover: int) -> str:
    if cloud_cover >= 70:
        return "☁️"
    if cloud_cover >= 40:
        return "🌤"
    return "☀️"


def _precipitation_icon(probability: int) -> str:
    if probability >= 50:
        return "🌧"
    if probability >= 20:
        return "🌦"
    return "☀️"


def _day_icon(is_day: int) -> str:
    return "☀️" if is_day else "🌙"


def format_current_weather(
    temp: float,
    wind: float,
    cloud_cover: int,
    precipitation_probability: int,
    is_day: int,
    sunrise: str,
    sunset: str,
) -> str:
    cloud_icon = _cloud_icon(cloud_cover)
    rain_icon = _precipitation_icon(precipitation_probability)
    day_icon = _day_icon(is_day)

    return (
        f"🌤 Сейчас\n\n"
        f"{day_icon} Температура: {temp:.1f}°\n"
        f"{cloud_icon} Облачность: {cloud_cover}%\n"
        f"{rain_icon} Дождь: {precipitation_probability}%\n"
        f"💨 Ветер: {wind:.1f} м/с\n"
        f"🌅 Восход: {sunrise}\n"
        f"🌇 Закат: {sunset}"
    )


def format_hourly_forecast(
    times: list[str],
    temps: list[float],
    cloud_cover: list[int],
    precipitation_probability: list[int],
    is_day: list[int],
) -> str:
    lines = ["🕒 Почасовой прогноз\n"]

    for time, temp, cloud, rain, day in zip(
        times,
        temps,
        cloud_cover,
        precipitation_probability,
        is_day,
    ):
        hour = time[11:16]
        day_icon = _day_icon(day)
        cloud_icon = _cloud_icon(cloud)
        rain_icon = _precipitation_icon(rain)
        lines.append(f"{hour}  {day_icon} {temp:.1f}°  {cloud_icon} {cloud}%  {rain_icon} {rain}%")

    return "\n".join(lines)
