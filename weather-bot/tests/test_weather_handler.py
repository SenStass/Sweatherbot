import asyncio
import unittest
from unittest.mock import patch

from handlers.weather import now


class WeatherHandlerTests(unittest.TestCase):
    @patch("handlers.weather.fetch_forecast")
    def test_now_handler_handles_missing_hourly_fields(self, mock_fetch_forecast) -> None:
        mock_fetch_forecast.return_value = {
            "hourly": {
                "temperature_2m": [],
                "wind_speed_10m": [],
                "cloud_cover": [],
                "precipitation_probability": [],
                "is_day": [],
            },
            "daily": {},
            "current_weather": {},
        }

        test_case = self

        async def fake_answer(message_obj, text: str) -> None:
            test_case.assertIn("Сейчас", text)

        message = type("Message", (), {"answer": fake_answer})()
        asyncio.run(now(message))


if __name__ == "__main__":
    unittest.main()
