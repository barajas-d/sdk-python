"""Unit tests for the Invoices resource using a mock HTTP client."""
import unittest

from tests.base_client_test import BaseClientTest


class TestInvoices(BaseClientTest):
    """Test Module: Invoices"""

    def test_search_authorized_payments(self):
        """Searches authorized payments using the documented query filters."""
        fixture = {"paging": {"total": 1}, "results": [{"id": "invoice-1"}]}
        filters = {
            "preapproval_id": "subscription-1",
            "payment_id": 123,
            "payer_id": 456,
            "status": "processed",
            "limit": 30,
            "offset": 0,
        }
        self.mock_get(fixture)

        result = self.sdk.invoices().search_authorized_payments(filters=filters)

        self.mock_http.get.assert_called_once()
        _, kwargs = self.mock_http.get.call_args
        self.assertEqual("https://api.mercadopago.com/authorized_payments", kwargs["url"])
        self.assertEqual(filters, kwargs["params"])
        self.assertEqual(200, result["status"])
        self.assertEqual(fixture, result["response"])


if __name__ == "__main__":
    unittest.main()