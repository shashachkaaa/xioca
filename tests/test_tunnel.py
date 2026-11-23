"""Regression tests for localhost.run tunnel URL parsing."""

import json
import unittest

from xioca.web.tunnel import extract_tunnel_url


def forward_event(host, **overrides):
    payload = {
        "event": "tcpip-forward",
        "status": "success",
        "address": host,
        "tls_termination": True,
    }
    payload.update(overrides)
    return json.dumps(payload)


class TunnelUrlTests(unittest.TestCase):
    def test_tunnel_lhr_life(self):
        self.assertEqual(
            extract_tunnel_url(forward_event("abc123.lhr.life")),
            "https://abc123.lhr.life",
        )

    def test_tunnel_localhost_run(self):
        self.assertEqual(
            extract_tunnel_url(forward_event("xyz987.localhost.run")),
            "https://xyz987.localhost.run",
        )

    def test_admin_link_in_ssh_banner_is_not_a_tunnel(self):
        self.assertIsNone(
            extract_tunnel_url("Visit https://admin.localhost.run for custom domains.")
        )

    def test_admin_host_is_rejected_even_in_success_event(self):
        self.assertIsNone(
            extract_tunnel_url(forward_event("admin.localhost.run"))
        )

    def test_other_events_are_rejected(self):
        self.assertIsNone(
            extract_tunnel_url(forward_event("abc123.lhr.life", event="welcome"))
        )

    def test_failed_forward_is_rejected(self):
        self.assertIsNone(
            extract_tunnel_url(forward_event("abc123.lhr.life", status="error"))
        )

    def test_missing_tls_is_rejected(self):
        self.assertIsNone(
            extract_tunnel_url(forward_event("abc123.lhr.life", tls_termination=False))
        )

    def test_untrusted_hostname_is_rejected(self):
        self.assertIsNone(
            extract_tunnel_url(forward_event("login.example.org"))
        )

    def test_alternative_listen_host_field(self):
        payload = json.dumps({
            "event": "tcpip-forward",
            "status": "success",
            "listen_host": "alt123.localhost.run",
            "tls_termination": True,
        })
        self.assertEqual(
            extract_tunnel_url(payload),
            "https://alt123.localhost.run",
        )


if __name__ == "__main__":
    unittest.main()
