"""Regression tests for the first step of web authorization."""

import asyncio
import tempfile
import unittest
from pathlib import Path
from unittest.mock import AsyncMock, Mock, patch

from starlette.requests import Request

from xioca.web.app import WebApp


def make_request(api_id: str, api_hash: str) -> Request:
    return Request({
        "type": "http",
        "method": "POST",
        "path": "/tokens",
        "root_path": "",
        "scheme": "http",
        "headers": [
            (b"id", api_id.encode("ascii")),
            (b"hash", api_hash.encode("ascii")),
        ],
        "query_string": b"",
        "server": ("127.0.0.1", 8080),
        "client": ("127.0.0.1", 12345),
        "http_version": "1.1",
    })


class WebCredentialsTests(unittest.TestCase):
    def test_invalid_api_id_returns_explanation(self):
        app = WebApp(session_name="test-invalid-api-id")
        with patch("xioca.web.app.Client") as client:
            response = asyncio.run(app.init_client(make_request("not-a-number", "a" * 32)))
            client.assert_not_called()

        self.assertEqual(response.status_code, 400)
        self.assertIn(b"API ID", response.body)

    def test_invalid_api_hash_returns_explanation(self):
        app = WebApp(session_name="test-invalid-api-hash")
        with patch("xioca.web.app.Client") as client:
            response = asyncio.run(app.init_client(make_request("12345", "not-a-hash")))
            client.assert_not_called()

        self.assertEqual(response.status_code, 400)
        self.assertIn(b"API Hash", response.body)

    def test_client_creation_failure_returns_error_not_http_200(self):
        app = WebApp(session_name="test-failed-connect")
        with patch("xioca.web.app.Client", side_effect=RuntimeError("mock connection error")):
            with patch("xioca.web.app.logging.exception"):
                response = asyncio.run(app.init_client(make_request("12345", "a" * 32)))

        self.assertEqual(response.status_code, 502)
        self.assertIn(b"RuntimeError", response.body)
        self.assertIsNone(app.client)

    def test_successful_connection_saves_config(self):
        app = WebApp(session_name="test-success-connect")
        client = Mock()
        client.is_connected = False
        client.connect = AsyncMock(return_value=False)
        with tempfile.TemporaryDirectory() as tempdir:
            config_path = Path(tempdir) / "config.ini"
            original_open = open

            def write_temp_config(path, *args, **kwargs):
                if path == "config.ini":
                    return original_open(config_path, *args, **kwargs)
                return original_open(path, *args, **kwargs)

            with patch("xioca.web.app.Client", return_value=client):
                with patch("xioca.web.app.open", side_effect=write_temp_config, create=True):
                    with patch("xioca.web.app.configparser.ConfigParser.read", return_value=[]):
                        response = asyncio.run(app.init_client(make_request("12345", "a" * 32)))

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.body, b"dialog")
            client.connect.assert_awaited_once()
            self.assertIn("api_id = 12345", config_path.read_text())
            self.assertIn("api_hash = " + "a" * 32, config_path.read_text())


if __name__ == "__main__":
    unittest.main()
