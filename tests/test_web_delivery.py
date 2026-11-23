"""Regression tests for Telegram's login-code delivery metadata."""

import asyncio
import json
import unittest
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock

from starlette.requests import Request

from xioca.web.app import WebApp, describe_code_delivery


def request_with_phone(phone="+12345678901"):
    body = json.dumps({"phone": phone}).encode("utf-8")
    async def receive():
        return {"type": "http.request", "body": body, "more_body": False}
    return Request({
        "type": "http",
        "method": "POST",
        "path": "/phone_request",
        "headers": [(b"content-type", b"application/json")],
        "query_string": b"",
    }, receive=receive)


def code_result(kind="APP", timeout=0, next_type=None, code_hash="hash1"):
    return SimpleNamespace(
        type=SimpleNamespace(name=kind),
        timeout=timeout,
        next_type=next_type,
        phone_code_hash=code_hash,
    )


class WebDeliveryTests(unittest.TestCase):
    def setUp(self):
        self.app = WebApp("test-code-flow")
        self.app.client = Mock()
        self.app.client.is_connected = True

    def test_channel_description_uses_telegram_sent_code_type(self):
        self.assertIn("Telegram", describe_code_delivery(SimpleNamespace(name="APP")))
        self.assertIn("SMS", describe_code_delivery(SimpleNamespace(name="SMS")))
        self.assertIn("email", describe_code_delivery(SimpleNamespace(name="EMAIL_CODE")))

    def test_channel_description_handles_raw_class_name(self):
        class SentCodeTypeApp:
            pass
        self.assertIn("Telegram", describe_code_delivery(SentCodeTypeApp))

    def test_send_code_returns_delivery_and_hash(self):
        self.app.client.send_code = AsyncMock(return_value=code_result(timeout=45, next_type="sms"))
        response = asyncio.run(self.app.send_code(request_with_phone()))
        result = json.loads(response.body)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(result["status"], "enter_code")
        self.assertTrue(result["can_resend"])
        self.assertEqual(result["retry_after"], 45)
        self.assertEqual(self.app.phone_code_hash, "hash1")
        self.app.client.send_code.assert_awaited_once_with("+12345678901")

    def test_no_next_type_means_no_resend_option(self):
        self.app.client.send_code = AsyncMock(return_value=code_result(next_type=None))
        response = asyncio.run(self.app.send_code(request_with_phone()))
        self.assertFalse(json.loads(response.body)["can_resend"])
        denied = asyncio.run(self.app.resend_code(request_with_phone()))
        self.assertEqual(denied.status_code, 409)

    def test_telegram_cooldown_is_enforced_on_server(self):
        self.app.client.send_code = AsyncMock(return_value=code_result(timeout=60, next_type="sms"))
        self.app.client.resend_code = AsyncMock()
        asyncio.run(self.app.send_code(request_with_phone()))

        denied = asyncio.run(self.app.resend_code(request_with_phone()))
        self.assertEqual(denied.status_code, 429)
        self.app.client.resend_code.assert_not_awaited()

    def test_resend_refreshes_code_hash_and_channel(self):
        self.app.client.send_code = AsyncMock(return_value=code_result(next_type="sms"))
        self.app.client.resend_code = AsyncMock(
            return_value=code_result(kind="SMS", code_hash="hash2", timeout=60)
        )
        asyncio.run(self.app.send_code(request_with_phone()))
        response = asyncio.run(self.app.resend_code(request_with_phone()))
        data = json.loads(response.body)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.app.phone_code_hash, "hash2")
        self.assertIn("SMS", data["delivery"])
        self.app.client.resend_code.assert_awaited_once_with("+12345678901", "hash1")

    def test_invalid_phone_is_not_sent_to_telegram(self):
        self.app.client.send_code = AsyncMock()
        response = asyncio.run(self.app.send_code(request_with_phone("bad-number")))
        self.assertEqual(response.status_code, 400)
        self.app.client.send_code.assert_not_awaited()


if __name__ == "__main__":
    unittest.main()
