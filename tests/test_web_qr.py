"""Regression tests for web-based Telegram QR authorization."""

import asyncio
import json
import time
import unittest
from unittest.mock import AsyncMock, Mock

from pyrogram import raw
from starlette.requests import Request

from xioca.web.app import WebApp


def get_request(path):
    return Request({
        "type": "http",
        "method": "GET",
        "path": path,
        "root_path": "",
        "scheme": "http",
        "headers": [],
        "query_string": b"",
        "server": ("127.0.0.1", 8080),
        "client": ("127.0.0.1", 12345),
        "http_version": "1.1",
    })


class WebQRTests(unittest.TestCase):
    def test_qr_requires_telegram_connection(self):
        async def scenario():
            app = WebApp("test-qr-no-connection")
            return await app.get_qr(get_request("/qrcode"))

        response = asyncio.run(scenario())
        self.assertEqual(response.status_code, 409)
        self.assertEqual(json.loads(response.body)["status"], "error")

    def test_qr_response_never_cached(self):
        app = WebApp("test-qr-headers")
        app.qr_status = "waiting"
        app.qr_image = "data:image/png;base64,AAAA"
        app.qr_link = "tg://login?token=abcd"
        response = app._qr_response()
        body = json.loads(response.body)
        self.assertEqual(response.headers["Cache-Control"], "no-store")
        self.assertEqual(body["status"], "waiting")
        self.assertEqual(body["link"], "tg://login?token=abcd")

    def test_qr_token_rotates_and_is_rendered_as_image(self):
        async def scenario():
            app = WebApp("test-qr-token")
            app.client = Mock()
            app.client.api_id = 12345
            app.client.api_hash = "a" * 32
            app.client.is_connected = True
            app.client.invoke = AsyncMock(return_value=raw.types.auth.LoginToken(
                expires=int(time.time()) + 30,
                token=b"temporary-token",
            ))
            app.qr_status = "waiting"
            task = asyncio.create_task(app._monitor_qr_login())
            try:
                for _ in range(80):
                    if app.qr_image:
                        break
                    if task.done():
                        break
                    await asyncio.sleep(0.025)
                self.assertEqual(app.qr_status, "waiting")
                self.assertTrue(app.qr_image.startswith("data:image/png;base64,"))
                self.assertTrue(app.qr_link.startswith("tg://login?token="))
                self.assertGreater(app.qr_expires, time.time())
            finally:
                task.cancel()
                await asyncio.gather(task, return_exceptions=True)

        asyncio.run(scenario())

    def test_qr_status_poll_does_not_generate_new_token(self):
        async def scenario():
            app = WebApp("test-qr-poll")
            app.qr_status = "waiting"
            app.qr_image = "data:image/png;base64,AAAA"
            app.qr_link = "tg://login?token=abcd"
            return await app.check_qr(get_request("/checkqr"))

        response = asyncio.run(scenario())
        self.assertEqual(json.loads(response.body)["image"], "data:image/png;base64,AAAA")


if __name__ == "__main__":
    unittest.main()
