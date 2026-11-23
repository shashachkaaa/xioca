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

    def test_explicitly_disabled_tls_is_rejected(self):
        self.assertIsNone(
            extract_tunnel_url(forward_event("abc123.lhr.life", tls_termination=False))
        )

    def test_optional_tls_field_can_be_missing(self):
        event = {"event": "tcpip-forward", "status": "success", "address": "abc123.lhr.life"}
        self.assertEqual(
            extract_tunnel_url(json.dumps(event)),
            "https://abc123.lhr.life",
        )

    def test_optional_status_field_can_be_missing(self):
        event = {"event": "tcpip-forward", "address": "abc123.lhr.life"}
        self.assertEqual(
            extract_tunnel_url(json.dumps(event)),
            "https://abc123.lhr.life",
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


    def test_real_localhost_run_cloudevent(self):
        # This shape is based on the SSH output observed on a Linux VPS.
        event = {
            "specversion": "1.0",
            "id": "test-registered-tunnel",
            "type": "run.localhost.tunnel.registered",
            "source": "ssh://localhost.run/sessions/example",
            "datacontenttype": "application/json",
            "subject": "206122dc3f83af.app.lhr.life",
            "data": {"address": "127.0.0.1"},
        }
        self.assertEqual(
            extract_tunnel_url(json.dumps(event)),
            "https://206122dc3f83af.app.lhr.life",
        )

    def test_cloudevent_with_data_address_when_subject_missing(self):
        event = {
            "specversion": "1.0",
            "type": "run.localhost.tunnel.registered",
            "data": {"address": "another123.app.lhr.life"},
        }
        self.assertEqual(
            extract_tunnel_url(json.dumps(event)),
            "https://another123.app.lhr.life",
        )

    def test_cloudevent_of_different_type_is_rejected(self):
        event = {
            "type": "run.localhost.tunnel.unregistered",
            "subject": "206122dc3f83af.app.lhr.life",
        }
        self.assertIsNone(extract_tunnel_url(json.dumps(event)))

    def test_admin_hostname_is_rejected_in_cloudevent(self):
        event = {
            "type": "run.localhost.tunnel.registered",
            "subject": "admin.localhost.run",
        }
        self.assertIsNone(extract_tunnel_url(json.dumps(event)))

    def test_unrelated_domain_is_rejected_in_cloudevent(self):
        event = {
            "type": "run.localhost.tunnel.registered",
            "subject": "example.com",
        }
        self.assertIsNone(extract_tunnel_url(json.dumps(event)))

    def test_blank_and_malformed_hostname_rejected(self):
        for hostname in ["", "abc..app.lhr.life", "https://abc.app.lhr.life", "*.lhr.life"]:
            event = {
                "type": "run.localhost.tunnel.registered",
                "subject": hostname,
            }
            self.assertIsNone(extract_tunnel_url(json.dumps(event)))


if __name__ == "__main__":
    unittest.main()
