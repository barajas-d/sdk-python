"""Unit tests for the QR Orders resource using a mock HTTP client."""
import json
import unittest

from tests.base_client_test import BaseClientTest


class TestQROrders(BaseClientTest):
    """Test Module: QR Orders."""

    def test_confirm_cashout_qr(self):
        self.mock_http.post.return_value = {
            "status": 200,
            "response": {"id": "123"},
        }
        payload = {"status": "confirmed"}

        result = self.sdk.qr_orders().confirm_cashout_qr("123", payload)

        self.mock_http.post.assert_called_once()
        _, kwargs = self.mock_http.post.call_args
        self.assertEqual(
            "https://api.mercadopago.com/instore/orders/123/confirmation",
            kwargs["url"],
        )
        self.assertEqual(payload, json.loads(kwargs["data"]))
        self.assertEqual(200, result["status"])


if __name__ == "__main__":
    unittest.main()