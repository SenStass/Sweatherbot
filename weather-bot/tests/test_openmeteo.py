import unittest
from unittest.mock import patch

import httpx

from services.openmeteo import fetch_model_temps


class OpenMeteoTests(unittest.TestCase):
    @patch("services.openmeteo.httpx.get")
    def test_fetch_model_temps_returns_multiple_models(self, mock_get) -> None:
        def fake_get(url, params=None, timeout=15.0):
            model_id = params.get("models", "default")
            temps = {
                "ecmwf_ifs025": 16.0,
                "icon_eu": 15.5,
                "gfs_seamless": 14.8,
                "arpEGE": 15.2,
            }
            temp = temps.get(model_id, 15.0)
            response = httpx.Response(200, json={"hourly": {"temperature_2m": [temp]}})
            response.request = httpx.Request("GET", url)
            return response

        mock_get.side_effect = fake_get

        temps = fetch_model_temps()

        self.assertEqual(temps["ecmwf"], 16.0)
        self.assertEqual(temps["icon-eu"], 15.5)
        self.assertEqual(temps["gfs"], 14.8)
        self.assertEqual(temps["arpEGE"], 15.2)


if __name__ == "__main__":
    unittest.main()
