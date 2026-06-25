import httpx

from config import LAT, LON

URL = "https://api.open-meteo.com/v1/forecast"

MODELS = {
    "ecmwf": "ecmwf_ifs025",
    "icon": "icon_seamless",
    "gfs": "gfs_seamless",
    "slav": "slav",
    "wrf": "wrf",
}


def fetch_forecast() -> dict:
    params = {
        "latitude": LAT,
        "longitude": LON,
        "hourly": [
            "temperature_2m",
            "precipitation_probability",
            "wind_speed_10m",
            "wind_direction_10m",
            "cloud_cover",
            "is_day",
            "weather_code",
            "apparent_temperature",
            "relative_humidity_2m",
        ],
        "current_weather": True,
        "timezone": "auto",
        "daily": [
            "sunrise",
            "sunset",
            "temperature_2m_max",
            "temperature_2m_min",
            "precipitation_probability_mean",
            "cloud_cover_mean",
        ],
        "forecast_days": 7,
    }

    response = httpx.get(URL, params=params, timeout=15.0)
    response.raise_for_status()
    data = response.json()

    if "hourly" not in data:
        reason = data.get("reason", "unknown error")
        raise RuntimeError(f"Open-Meteo error: {reason}")

    return data


def _current_temperature(data: dict) -> float:
    for value in data["hourly"]["temperature_2m"]:
        if value is not None:
            return float(value)
    raise RuntimeError("No temperature data in forecast")


def fetch_model_temps() -> dict[str, float]:
    temps: dict[str, float] = {}

    for name, model_id in MODELS.items():
        params = {
            "latitude": LAT,
            "longitude": LON,
            "hourly": "temperature_2m",
            "forecast_days": 1,
            "models": model_id,
        }
        try:
            response = httpx.get(URL, params=params, timeout=15.0)
            response.raise_for_status()
            data = response.json()
        except Exception:
            continue

        if "hourly" not in data:
            reason = data.get("reason", "unknown error")
            continue

        temps[name] = _current_temperature(data)

    return temps
