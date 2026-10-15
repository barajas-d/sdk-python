"""
    Module: test_payment_methods
"""
import os
import unittest
import mercadopago
from mercadopago.config import RequestOptions
from mercadopago.http import HttpClient


class FakeHttpClient(HttpClient):
    """Captures installment GETs without making network requests."""

    def __init__(self):
        self.get_calls = []
        self.installments = [{
            "payment_method_id": "visa",
            "issuer": {"id": 1, "name": "Issuer"},
            "payer_costs": [{"installments": 3, "installment_amount": 50.0}],
        }]

    def get(self, url, headers, params=None, timeout=None, maxretries=None):
        self.get_calls.append({
            "url": url,
            "headers": headers,
            "params": params,
            "timeout": timeout,
            "maxretries": maxretries,
        })
        return {"status": 200, "response": self.installments}


class TestPaymentMethods(unittest.TestCase):
    """
    Test Module: Payment Methods
    """

    def test_find(self):
        """
        Test Function: Payment Methods
        """
        sdk = mercadopago.SDK(os.environ['ACCESS_TOKEN'])
        self.assertEqual(sdk.payment_methods().list_all()["status"], 200)

    def test_get_installments_forwards_required_and_optional_query_without_body(self):
        """GET installments retains the resource's status/response envelope."""
        client = FakeHttpClient()
        sdk = mercadopago.SDK("TEST_ACCESS_TOKEN", http_client=client)
        options = RequestOptions(custom_headers={"x-test-header": "installments"})

        result = sdk.payment_methods().get_installments(
            "visa", 150.0, issuer_id="1", bin="411111", request_options=options
        )

        self.assertEqual(result, {"status": 200, "response": client.installments})
        self.assertEqual(len(client.get_calls), 1)
        call = client.get_calls[0]
        self.assertEqual(call["url"],
                         "https://api.mercadopago.com/v1/payment_methods/installments")
        self.assertEqual(call["params"], {
            "payment_method_id": "visa", "amount": 150.0,
            "issuer_id": "1", "bin": "411111",
        })
        self.assertNotIn("data", call)
        self.assertEqual(call["headers"]["x-test-header"], "installments")

        result = sdk.payment_methods().get_installments("master", 0.0)
        self.assertEqual(result, {"status": 200, "response": client.installments})
        self.assertEqual(client.get_calls[1]["params"], {
            "payment_method_id": "master", "amount": 0.0,
        })
        self.assertNotIn("data", client.get_calls[1])


if __name__ == "__main__":
    unittest.main()