import asyncio
import unittest
from unittest.mock import patch

from handlers.weather import now


class WeatherHandlerTests(unittest.TestCase):
    def test_now_handler_returns_unavailable_message(self) -> None:
        test_case = self

        async def fake_answer(message_obj, text: str) -> None:
            test_case.assertIn("временно недоступны", text)

        message = type("Message", (), {"answer": fake_answer})()
        asyncio.run(now(message))


if __name__ == "__main__":
    unittest.main()
