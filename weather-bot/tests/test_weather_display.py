import unittest

from handlers.weather import build_hourly_forecast_payload, get_daily_forecast_value
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
            humidity=58,
            apparent_temperature=17.2,
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
        self.assertNotIn("07:10:00 01.01.2024", text)
        self.assertNotIn("17:40:00 01.01.2024", text)
        self.assertIn("🌧️", text)
        self.assertIn("💧", text)
        self.assertIn("58%", text)
        self.assertIn("🫠", text)
        self.assertIn("17.2°", text)
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
        self.assertIn("⛅", text)
        self.assertIn("☁️", text)
        self.assertIn("🌧️", text)

    def test_hourly_forecast_uses_column_separators(self) -> None:
        text = format_hourly_forecast(
            times=["2024-01-01T12:00"],
            temps=[18.4],
            cloud_cover=[40],
            precipitation_probability=[10],
            is_day=[1],
            apparent_temperature=[19.0],
            humidity=[45],
            wind_speed=[4.0],
        )

        self.assertIn("Время", text)
        self.assertIn("Темп.", text)
        self.assertIn("12:00", text)

    def test_build_hourly_forecast_payload_from_meteoinfo(self) -> None:
        payload = build_hourly_forecast_payload(
            [
                {
                    "time": "12:00",
                    "temperature": 14.2,
                    "precipitation": 1.0,
                    "wind": 3.0,
                    "humidity": 58,
                    "cloudiness": 70,
                }
            ]
        )

        self.assertEqual(payload["times"], ["2024-01-01T12:00"])
        self.assertEqual(payload["temps"], [14.2])
        self.assertEqual(payload["cloud_cover"], [70])
        self.assertEqual(payload["precipitation_probability"], [10])
        self.assertEqual(payload["humidity"], [58])
        self.assertEqual(payload["wind_speed"], [3.0])

    def test_weekly_forecast_includes_day_summary(self) -> None:
        text = format_weekly_forecast(
            dates=["2024-01-01", "2024-01-02"],
            max_temps=[18.4, 19.1],
            min_temps=[10.2, 11.1],
            precipitation_probability=[20, 80],
            cloud_cover=[40, 80],
        )

        self.assertIn("Прогноз на 7 дней", text)
        self.assertIn("Дата", text)
        self.assertIn("Макс", text)
        self.assertIn("Мин", text)
        self.assertIn("Обл.", text)
        self.assertIn("Осадки", text)
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
            sunrise="2024-01-01T07:10",
            sunset="2024-01-01T17:40",
        )

        self.assertIn("Сегодня", text)
        self.assertIn("18.4°", text)
        self.assertIn("10.2°", text)
        self.assertIn("40%", text)
        self.assertIn("20%", text)
        self.assertIn("07:10", text)
        self.assertIn("17:40", text)

    def test_get_daily_forecast_value_handles_missing_day(self) -> None:
        data = {"daily": {"time": ["2024-01-01"], "temperature_2m_max": [18.4]}}

        value = get_daily_forecast_value(data, "temperature_2m_max", 1)

        self.assertEqual(value, None)


if __name__ == "__main__":
    unittest.main()
