"""
    Module: test_payment_methods
"""
import os
import unittest
import mercadopago


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

    def test_get_installments(self):
        """Checks the installments endpoint and its query parameters."""
        from unittest.mock import MagicMock
        from mercadopago.http.http_client import HttpClient

        mock_http = MagicMock(spec=HttpClient)
        mock_http.get.return_value = {"status": 200, "response": [{"payment_method_id": "visa"}]}
        sdk = mercadopago.SDK("TEST_ACCESS_TOKEN", http_client=mock_http)

        result = sdk.payment_methods().get_installments(
            "visa", 1000.0, issuer_id="123", bin="411111")

        mock_http.get.assert_called_once()
        args, kwargs = mock_http.get.call_args
        self.assertEqual((), args)
        self.assertEqual("https://api.mercadopago.com/v1/payment_methods/installments",
                         kwargs["url"])
        self.assertEqual({"payment_method_id": "visa", "amount": 1000.0,
                          "issuer_id": "123", "bin": "411111"}, kwargs["params"])
        self.assertEqual(200, result["status"])


if __name__ == "__main__":
    unittest.main()
