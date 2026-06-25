import unittest

from services.display import format_current_weather, format_hourly_forecast


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
        )

        self.assertIn("☀️", text)
        self.assertIn("☁️", text)
        self.assertIn("🌧", text)
        self.assertIn("18.4°", text)

    def test_hourly_forecast_includes_icons_per_hour(self) -> None:
        text = format_hourly_forecast(
            times=["2024-01-01T12:00", "2024-01-01T13:00"],
            temps=[18.4, 19.1],
            cloud_cover=[40, 80],
            precipitation_probability=[10, 70],
            is_day=[1, 0],
        )

        self.assertIn("12:00", text)
        self.assertIn("13:00", text)
        self.assertIn("☀️", text)
        self.assertIn("🌙", text)
        self.assertIn("🌤", text)
        self.assertIn("☁️", text)
        self.assertIn("🌧", text)


if __name__ == "__main__":
    unittest.main()
