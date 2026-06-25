from meteostat import Point, Hourly
from datetime import datetime
from config import LAT, LON

def get_actual_weather():
    location = Point(LAT, LON)

    start = datetime.utcnow()
    end = datetime.utcnow()

    data = Hourly(location, start, end)
    data = data.fetch()

    if data.empty:
        return None

    last = data.iloc[-1]

    return {
        "temp": float(last["temp"]),
        "wind": float(last["wspd"]),
        "pressure": float(last["pres"])
    }