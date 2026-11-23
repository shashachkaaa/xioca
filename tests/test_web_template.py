"""Ensure the login panel renders with modern Starlette releases."""

import asyncio
import unittest

from starlette.requests import Request

from xioca.web.app import WebApp


class WebTemplateTests(unittest.TestCase):
    def test_index_renders_without_internal_server_error(self):
        app = WebApp(session_name="test-web-template")
        request = Request({
            "type": "http",
            "method": "GET",
            "path": "/",
            "root_path": "",
            "scheme": "http",
            "headers": [],
            "query_string": b"",
            "server": ("127.0.0.1", 8080),
            "client": ("127.0.0.1", 12345),
            "http_version": "1.1",
        })

        response = asyncio.run(app.index(request))

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"<title>Xioca Authorization</title>", response.body)


if __name__ == "__main__":
    unittest.main()
