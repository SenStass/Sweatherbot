import unittest

from handlers.weather import get_daily_forecast_value
from services.display import (
    format_current_weather,
    format_day_forecast,
    format_hourly_forecast,
    format_weekly_forecast,
)


class WeatherDisplayTests(unittest.TestCase):
    def test_current_weather_includes_sun_cloud_and_rain_icons(self) -> None:
        text = format_current_weather(
            temp=18.4,
            wind=4.2,
            cloud_cover=75,
            precipitation_probability=60,
            is_day=1,
            sunrise="2024-01-01T07:10",
            sunset="2024-01-01T17:40",
            weather_code=80,
            wind_direction=180,
            local_time="2024-01-01T12:34:56",
        )

        self.assertIn("☀️", text)
        self.assertIn("☁️", text)
        self.assertIn("🌧️", text)
        self.assertIn("18.4°", text)
        self.assertIn("07:10:00 01.01.2024", text)
        self.assertIn("17:40:00 01.01.2024", text)
        self.assertIn("🌧️", text)
        self.assertIn("⬇️", text)
        self.assertIn("🟡", text)
        self.assertIn("12:34", text)

    def test_hourly_forecast_includes_icons_per_hour(self) -> None:
        text = format_hourly_forecast(
            times=["2024-01-01T12:00", "2024-01-01T13:00"],
            temps=[18.4, 19.1],
            cloud_cover=[40, 80],
            precipitation_probability=[10, 70],
            is_day=[1, 0],
            apparent_temperature=[19.0, 18.5],
            humidity=[45, 55],
            wind_speed=[4.0, 6.0],
        )

        self.assertIn("12:00", text)
        self.assertIn("13:00", text)
        self.assertIn("☀️", text)
        self.assertIn("🌙", text)
        self.assertIn("⛅", text)
        self.assertIn("☁️", text)
        self.assertIn("🌧️", text)

    def test_weekly_forecast_includes_day_summary(self) -> None:
        text = format_weekly_forecast(
            dates=["2024-01-01", "2024-01-02"],
            max_temps=[18.4, 19.1],
            min_temps=[10.2, 11.1],
            precipitation_probability=[20, 80],
            cloud_cover=[40, 80],
        )

        self.assertIn("Прогноз на 7 дней", text)
        self.assertIn("01.01", text)
        self.assertIn("02.01", text)
        self.assertIn("⛅", text)
        self.assertIn("☁️", text)
        self.assertIn("🌦", text)
        self.assertIn("🌧️", text)

    def test_day_forecast_includes_title_and_metrics(self) -> None:
        text = format_day_forecast(
            title="☀️ Сегодня",
            date="2024-01-01",
            max_temp=18.4,
            min_temp=10.2,
            precipitation_probability=20,
            cloud_cover=40,
            weather_code=1,
        )

        self.assertIn("Сегодня", text)
        self.assertIn("18.4°", text)
        self.assertIn("10.2°", text)
        self.assertIn("40%", text)
        self.assertIn("20%", text)

    def test_get_daily_forecast_value_handles_missing_day(self) -> None:
        data = {"daily": {"time": ["2024-01-01"], "temperature_2m_max": [18.4]}}

        value = get_daily_forecast_value(data, "temperature_2m_max", 1)

        self.assertEqual(value, None)


if __name__ == "__main__":
    unittest.main()
