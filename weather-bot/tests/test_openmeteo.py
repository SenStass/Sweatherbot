import unittest
from unittest.mock import patch

import httpx

from services.openmeteo import fetch_model_temps


class OpenMeteoTests(unittest.TestCase):
    @patch("services.openmeteo.httpx.get")
    def test_fetch_model_temps_includes_slav_and_wrf(self, mock_get) -> None:
        def fake_get(url, params=None, timeout=15.0):
            model_id = params.get("models")
            temp = 12.3
            if model_id == "slav":
                temp = 11.5
            elif model_id == "wrf":
                temp = 13.0

            response = httpx.Response(200, json={"hourly": {"temperature_2m": [temp]}})
            response.request = httpx.Request("GET", url)
            return response

        mock_get.side_effect = fake_get

        with patch("services.openmeteo.MODELS", {
            "ecmwf": "ecmwf_ifs025",
            "slav": "slav",
            "wrf": "wrf"
        }):
            temps = fetch_model_temps()

        self.assertEqual(temps["ecmwf"], 12.3)
        self.assertEqual(temps["slav"], 11.5)
        self.assertEqual(temps["wrf"], 13.0)


if __name__ == "__main__":
    unittest.main()
