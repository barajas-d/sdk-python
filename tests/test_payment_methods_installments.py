"""Offline tests for payment-method installments."""
import unittest

from mercadopago import SDK
from mercadopago.config import RequestOptions
from mercadopago.http import HttpClient


class FakeHttpClient(HttpClient):
    """Records GET requests without calling the API."""

    def __init__(self):
        self.calls = []

    def get(self, url, headers, params=None, timeout=None, maxretries=None):
        self.calls.append({"url": url, "headers": headers, "params": params,
                           "timeout": timeout, "maxretries": maxretries})
        return {"status": 200, "response": [{"payment_method_id": "visa",
                                              "issuer": {"id": 1}, "payer_costs": []}]}


class TestPaymentMethodsInstallments(unittest.TestCase):
    """Checks installment query parameters and per-call options."""

    def test_required_parameters_and_response(self):
        client = FakeHttpClient()
        sdk = SDK("TEST_ACCESS_TOKEN", http_client=client)
        response = sdk.payment_methods().get_installments("visa", 1000.0)

        self.assertEqual(client.calls[0]["url"],
                         "https://api.mercadopago.com/v1/payment_methods/installments")
        self.assertEqual(client.calls[0]["params"],
                         {"payment_method_id": "visa", "amount": 1000.0})
        self.assertEqual(response["status"], 200)
        self.assertEqual(response["response"][0]["payment_method_id"], "visa")

    def test_optional_parameters_and_request_options(self):
        client = FakeHttpClient()
        sdk = SDK("TEST_ACCESS_TOKEN", http_client=client)
        options = RequestOptions(connection_timeout=12.0, max_retries=2,
                                 custom_headers={"X-Test": "per-call"})
        sdk.payment_methods().get_installments(
            "visa", 0.0, issuer_id="123", bin="411111", request_options=options)

        call = client.calls[0]
        self.assertEqual(call["params"], {"payment_method_id": "visa", "amount": 0.0,
                                          "issuer_id": "123", "bin": "411111"})
        self.assertEqual(call["headers"]["X-Test"], "per-call")
        self.assertEqual(call["headers"]["Authorization"], "Bearer TEST_ACCESS_TOKEN")
        self.assertEqual(call["timeout"], 12.0)
        self.assertEqual(call["maxretries"], 2)

    def test_list_all_remains_separate(self):
        client = FakeHttpClient()
        SDK("TEST_ACCESS_TOKEN", http_client=client).payment_methods().list_all()
        self.assertEqual(client.calls[0]["url"],
                         "https://api.mercadopago.com/v1/payment_methods")
        self.assertIsNone(client.calls[0]["params"])


if __name__ == "__main__":
    unittest.main()