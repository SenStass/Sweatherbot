import unittest
from unittest.mock import patch

import httpx

from services.openmeteo import fetch_model_temps


class OpenMeteoTests(unittest.TestCase):
    @patch("services.openmeteo.httpx.get")
    def test_fetch_model_temps_skips_invalid_models(self, mock_get) -> None:
        def fake_get(url, params=None, timeout=15.0):
            model_id = params.get("models")
            if model_id == "slav":
                raise httpx.HTTPError("Bad Request")

            response = httpx.Response(200, json={"hourly": {"temperature_2m": [12.3]}})
            response.request = httpx.Request("GET", url)
            return response

        mock_get.side_effect = fake_get

        with patch("services.openmeteo.MODELS", {"ecmwf": "ecmwf_ifs025", "slav": "slav"}):
            temps = fetch_model_temps()

        self.assertEqual(temps, {"ecmwf": 12.3})
        self.assertNotIn("slav", temps)


if __name__ == "__main__":
    unittest.main()
