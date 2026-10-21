"""Unit tests for the Terminals resource using a mock HTTP client."""
import json
import unittest

from tests.base_client_test import BaseClientTest


class TestTerminals(BaseClientTest):
    """Test Module: Terminals"""

    def test_get_terminal_action(self):
        """Fetches an action using GET without a request payload."""
        self.mock_get({"id": "action-1", "status": "pending"})

        result = self.sdk.terminals().get_terminal_action("action-1")

        self.mock_http.get.assert_called_once()
        _, kwargs = self.mock_http.get.call_args
        self.assertEqual(
            "https://api.mercadopago.com/terminals/v1/actions/action-1",
            kwargs["url"])
        self.assertNotIn("data", kwargs)
        self.assertEqual(200, result["status"])

    def test_list_terminals(self):
        """Lists terminals using GET without a request payload."""
        self.mock_get({"terminals": [{"id": "device-1"}]})

        result = self.sdk.terminals().list_terminals()

        self.mock_http.get.assert_called_once()
        _, kwargs = self.mock_http.get.call_args
        self.assertEqual(
            "https://api.mercadopago.com/terminals/v1/list", kwargs["url"])
        self.assertNotIn("data", kwargs)
        self.assertEqual(200, result["status"])

    def test_create_terminal_action(self):
        """Creates a print action using POST with the JSON print payload."""
        self.mock_post({"id": "action-1", "status": "pending"}, status=200)
        payload = {
            "type": "PRINT_INFO",
            "external_reference": "print-1",
            "config": {"device_id": "device-1"},
            "content": {"source": "https://example.com/receipt.png"},
        }

        result = self.sdk.terminals().create_terminal_action(payload)

        self.mock_http.post.assert_called_once()
        _, kwargs = self.mock_http.post.call_args
        self.assertEqual(
            "https://api.mercadopago.com/terminals/v1/actions", kwargs["url"])
        self.assertEqual(payload, json.loads(kwargs["data"]))
        self.assertEqual(200, result["status"])

    def test_cancel_terminal_action(self):
        """Cancels an action using POST without a request payload."""
        self.mock_post(None, status=200)

        result = self.sdk.terminals().cancel_terminal_action("action-1")

        self.mock_http.post.assert_called_once()
        _, kwargs = self.mock_http.post.call_args
        self.assertEqual(
            "https://api.mercadopago.com/terminals/v1/actions/action-1/cancel",
            kwargs["url"])
        self.assertIsNone(kwargs["data"])
        self.assertEqual(200, result["status"])

    def test_cancel_point_refund_intent(self):
        """Cancel uses DELETE with both path parameters and no request body."""
        self.mock_delete(None)

        result = self.sdk.terminals().cancel_point_refund_intent(
            "device-1", "refund-2")

        self.mock_http.delete.assert_called_once()
        _, kwargs = self.mock_http.delete.call_args
        self.assertEqual(
            "https://api.mercadopago.com/point/integration-api/"
            "devices/device-1/refund/refund-2", kwargs["url"])
        self.assertNotIn("data", kwargs)
        self.assertEqual(204, result["status"])

    def test_get_point_refund_intent(self):
        """Fetches a refund intent with GET and no request body."""
        self.mock_get({"id": "refund-2", "status": "approved"})

        result = self.sdk.terminals().get_point_refund_intent("refund-2")

        self.mock_http.get.assert_called_once()
        _, kwargs = self.mock_http.get.call_args
        self.assertEqual(
            "https://api.mercadopago.com/point/integration-api/"
            "refund/refund-2", kwargs["url"])
        self.assertNotIn("data", kwargs)
        self.assertEqual(200, result["status"])

    def test_create_point_refund_intent(self):
        """A partial refund sends its payment ID and optional amount."""
        self.mock_post({"id": "refund-1", "status": "created"}, status=200)
        payload = {"payment_id": 123, "amount": 10.5}

        result = self.sdk.terminals().create_point_refund_intent(
            "device-1", payload)

        self.mock_http.post.assert_called_once()
        _, kwargs = self.mock_http.post.call_args
        self.assertEqual(
            "https://api.mercadopago.com/point/integration-api/"
            "devices/device-1/refund", kwargs["url"])
        self.assertEqual(payload, json.loads(kwargs["data"]))
        self.assertEqual(200, result["status"])

    def test_update_terminal_operation_mode(self):
        """Updates terminal operating modes using JSON PATCH."""
        self.mock_http.request.return_value = {
            "status": 200, "response": {"id": "device-1"}}
        payload = {"terminals": [
            {"id": "device-1", "operating_mode": "PDV"},
            {"id": "device-2", "operating_mode": "STANDALONE"},
        ]}

        result = self.sdk.terminals().update_terminal_operation_mode(payload)

        self.mock_http.request.assert_called_once()
        args, kwargs = self.mock_http.request.call_args
        self.assertEqual(("PATCH",), args)
        self.assertEqual(
            "https://api.mercadopago.com/terminals/v1/setup", kwargs["url"])
        self.assertEqual(payload, json.loads(kwargs["data"]))
        self.assertEqual(200, result["status"])

    def test_create_point_refund_intent_full_refund(self):
        """A full refund requires only the payment ID."""
        self.mock_post({"id": "refund-2", "status": "created"}, status=200)
        payload = {"payment_id": 123}

        result = self.sdk.terminals().create_point_refund_intent(
            "device-1", payload)

        self.mock_http.post.assert_called_once()
        _, kwargs = self.mock_http.post.call_args
        self.assertEqual(
            "https://api.mercadopago.com/point/integration-api/"
            "devices/device-1/refund", kwargs["url"])
        self.assertEqual(payload, json.loads(kwargs["data"]))
        self.assertEqual(200, result["status"])


if __name__ == "__main__":
    unittest.main()