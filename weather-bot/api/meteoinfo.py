from __future__ import annotations

import re
from datetime import datetime, timedelta
from typing import Optional

import aiohttp
from bs4 import BeautifulSoup

DEFAULT_REGION = "belgorodskaya-area"
DEFAULT_CITY = "belgorod"
CACHE_TTL_SECONDS = 30 * 60

_cache: dict[tuple[str, str], tuple[datetime, list[dict[str, object]]]] = {}


async def fetch_meteoinfo_forecast(
    region: str = DEFAULT_REGION,
    city: str = DEFAULT_CITY,
    *,
    ttl_seconds: int = CACHE_TTL_SECONDS,
) -> list[dict[str, object]]:
    cache_key = (region, city)
    now = datetime.now()
    cached = _cache.get(cache_key)
    if cached is not None and now - cached[0] < timedelta(seconds=ttl_seconds):
        return cached[1]

    url = f"https://meteoinfo.ru/pogoda/russia/{region}/{city}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url, timeout=20) as response:
            response.raise_for_status()
            html = await response.text()

    soup = BeautifulSoup(html, "html.parser")
    rows = _extract_hourly_rows(soup)
    if not rows:
        raise RuntimeError("No hourly forecast data found on meteoinfo page")

    _cache[cache_key] = (now, rows)
    return rows


def _extract_hourly_rows(soup: BeautifulSoup) -> list[dict[str, object]]:
    tables = soup.find_all("table")
    rows: list[dict[str, object]] = []

    for table in tables:
        headers = [th.get_text(" ", strip=True).lower() for th in table.find_all("th")]
        if not headers:
            continue

        cells = table.find_all("tr")
        for row in cells[1:]:
            values = [td.get_text(" ", strip=True) for td in row.find_all("td")]
            if not values:
                continue

            if _looks_like_hourly_row(headers, values):
                item = _parse_hourly_row(values)
                if item is not None:
                    rows.append(item)

    return rows


def _looks_like_hourly_row(headers: list[str], values: list[str]) -> bool:
    if not headers or len(values) < 5:
        return False

    joined = " ".join(headers).lower()
    if "время" in joined or "час" in joined or "time" in joined:
        return True

    return any(re.search(r"\d{1,2}:\d{2}", value) for value in values)


def _parse_hourly_row(values: list[str]) -> Optional[dict[str, object]]:
    if not values:
        return None

    cleaned = [re.sub(r"\s+", " ", value).strip() for value in values]
    if not cleaned:
        return None

    time_value = None
    temp_value = None
    rain_value = None
    wind_value = None
    humidity_value = None
    cloud_value = None

    for value in cleaned:
        if re.fullmatch(r"\d{1,2}:\d{2}", value):
            time_value = value
        elif re.search(r"[-+]?\d+(?:[.,]\d+)?", value) and "°" in value:
            temp_value = re.sub(r"[^0-9,.-]", "", value)
        elif re.search(r"\d+", value) and "%" in value:
            if humidity_value is None:
                humidity_value = re.sub(r"[^0-9]", "", value)
            else:
                cloud_value = re.sub(r"[^0-9]", "", value)
        elif re.search(r"\d+", value) and ("м/с" in value or "мс" in value):
            wind_value = re.sub(r"[^0-9,.-]", "", value)
        elif re.search(r"\d+", value) and ("мм" in value or "м" in value.lower()):
            rain_value = re.sub(r"[^0-9]", "", value)

    if time_value is None:
        return None

    return {
        "time": time_value,
        "temperature": float(temp_value.replace(",", ".")) if temp_value else None,
        "precipitation": float(rain_value) if rain_value else None,
        "wind": float(wind_value.replace(",", ".")) if wind_value else None,
        "humidity": int(humidity_value) if humidity_value else None,
        "cloudiness": int(cloud_value) if cloud_value else None,
    }
