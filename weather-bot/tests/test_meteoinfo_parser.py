import asyncio
import unittest
from unittest.mock import patch

from api.meteoinfo import fetch_meteoinfo_forecast


class MeteoinfoParserTests(unittest.TestCase):
    def test_fetch_meteoinfo_forecast_parses_hourly_rows(self) -> None:
        class FakeResponse:
            async def __aenter__(self):
                return self

            async def __aexit__(self, exc_type, exc, tb):
                return False

            async def text(self):
                return """
                <html><body>
                <table>
                    <tr><th>Время</th><th>Температура</th><th>Осадки</th><th>Ветер</th><th>Влажность</th><th>Облачность</th></tr>
                    <tr><td>12:00</td><td>+14.2°</td><td>1 мм</td><td>3 м/с</td><td>58%</td><td>70%</td></tr>
                </table>
                </body></html>
                """

            raise_for_status = lambda self: None

        class FakeSession:
            async def __aenter__(self):
                return self

            async def __aexit__(self, exc_type, exc, tb):
                return False

            def get(self, url, timeout):
                return FakeResponse()

        async def run_test() -> list[dict[str, object]]:
            with patch("api.meteoinfo.aiohttp.ClientSession", return_value=FakeSession()):
                return await fetch_meteoinfo_forecast(region="belgorodskaya-area", city="belgorod")

        data = asyncio.run(run_test())

        self.assertEqual(data[0]["time"], "12:00")
        self.assertEqual(data[0]["temperature"], 14.2)
        self.assertEqual(data[0]["precipitation"], 1.0)
        self.assertEqual(data[0]["wind"], 3.0)
        self.assertEqual(data[0]["humidity"], 58)
        self.assertEqual(data[0]["cloudiness"], 70)


if __name__ == "__main__":
    unittest.main()
