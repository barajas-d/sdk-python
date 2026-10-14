"""
    Module: test_payment_methods
"""
import os
import unittest
from unittest.mock import patch

import mercadopago
from mercadopago.config import RequestOptions
from mercadopago.http import HttpClient


class TestPaymentMethods(unittest.TestCase):
    """
    Test Module: Payment Methods
    """
    sdk = mercadopago.SDK(os.environ['ACCESS_TOKEN'])

    def test_find(self):
        """
        Test Function: Payment Methods
        """
        self.assertEqual(self.sdk.payment_methods().list_all()["status"], 200)

    def test_get_installments_required_query(self):
        """GET installments sends required fields in query and returns HTTP result."""
        response = {"status": 200, "response": [{"payment_method_id": "visa",
                                                 "payer_costs": [{"installments": 3}]}]}
        with patch.object(HttpClient, "get", return_value=response) as get:
            sdk = mercadopago.SDK("TEST_ACCESS_TOKEN")
            result = sdk.payment_methods().get_installments("visa", 1000.0)

        self.assertIs(result, response)
        get.assert_called_once()
        kwargs = get.call_args.kwargs
        self.assertEqual(kwargs["url"],
                         "https://api.mercadopago.com/v1/payment_methods/installments")
        self.assertEqual(kwargs["params"], {"payment_method_id": "visa", "amount": 1000.0})
        self.assertNotIn("data", kwargs)

    def test_get_installments_optional_query_and_request_options(self):
        """Optional filters and per-call options reach the HTTP client."""
        options = RequestOptions(connection_timeout=12.0, max_retries=1,
                                 custom_headers={"x-test-header": "installments"})
        with patch.object(HttpClient, "get", return_value={"status": 200,
                                                            "response": []}) as get:
            sdk = mercadopago.SDK("TEST_ACCESS_TOKEN")
            sdk.payment_methods().get_installments(
                "master", 150.0, issuer_id="123", bin="411111", request_options=options)

        kwargs = get.call_args.kwargs
        self.assertEqual(kwargs["params"], {"payment_method_id": "master",
                                            "amount": 150.0, "issuer_id": "123",
                                            "bin": "411111"})
        self.assertEqual(kwargs["headers"]["x-test-header"], "installments")
        self.assertEqual(kwargs["headers"]["Authorization"], "Bearer TEST_ACCESS_TOKEN")
        self.assertEqual(kwargs["timeout"], 12.0)
        self.assertEqual(kwargs["maxretries"], 1)
        self.assertNotIn("data", kwargs)


if __name__ == "__main__":
    unittest.main()
