"""Unit tests for the Payouts resource using a mock HTTP client."""
import json
import unittest

from mercadopago.config import RequestOptions
from mercadopago.resources import Payouts
from tests.base_client_test import BaseClientTest


class TestPayouts(BaseClientTest):
    """Test Module: Payouts"""

    def test_create_payout(self):
        """A payout batch is submitted as JSON to the payouts endpoint."""
        payload = {
            "external_reference": "batch-001",
            "transactions": [{
                "amount": 100.0,
                "beneficiary": {"id": "recipient-001"},
                "currency_id": "BRL",
                "payment_method_id": "pix",
            }],
        }
        self.mock_http.post.return_value = {
            "status": 201, "response": {"id": "batch-001"}}

        result = self.sdk.payouts().create_payout(payload)

        self.mock_http.post.assert_called_once()
        args, kwargs = self.mock_http.post.call_args
        self.assertEqual((), args)
        self.assertEqual("https://api.mercadopago.com/v1/payouts", kwargs["url"])
        self.assertEqual(payload, json.loads(kwargs["data"]))
        self.assertEqual(201, result["status"])

    def test_process_transaction_intent(self):
        """A transaction intent is submitted as JSON to its process endpoint."""
        payload = {
            "external_reference": "PAYOUT-001",
            "point_of_interaction": {"type": "PIX"},
            "transaction": {"amount": 100.0, "currency_id": "BRL"},
        }
        self.mock_http.post.return_value = {
            "status": 201, "response": {"id": "intent-001"}}

        result = self.sdk.payouts().process_transaction_intent(payload)

        self.mock_http.post.assert_called_once()
        args, kwargs = self.mock_http.post.call_args
        self.assertEqual((), args)
        self.assertEqual("https://api.mercadopago.com/v1/transaction-intents/process",
                         kwargs["url"])
        self.assertEqual(payload, json.loads(kwargs["data"]))
        self.assertEqual(201, result["status"])

    def test_list_payout_transactions(self):
        """GET lists transactions without sending a JSON payload."""
        self.mock_get({"transactions": [{"id": "txn-001"}]})

        result = self.sdk.payouts().list_payout_transactions("batch/001")

        self.mock_http.get.assert_called_once()
        args, kwargs = self.mock_http.get.call_args
        self.assertEqual((), args)
        self.assertEqual("https://api.mercadopago.com/v1/payouts/batch%2F001/transactions",
                         kwargs["url"])
        self.assertNotIn("data", kwargs)
        self.assertEqual(200, result["status"])

    def test_get_transaction_intent(self):
        """GET retrieves an intent without sending a JSON payload."""
        self.mock_get({"id": "intent-001"})

        result = self.sdk.payouts().get_transaction_intent("intent/001")

        self.mock_http.get.assert_called_once()
        args, kwargs = self.mock_http.get.call_args
        self.assertEqual((), args)
        self.assertEqual("https://api.mercadopago.com/v1/transaction-intents/intent%2F001",
                         kwargs["url"])
        self.assertNotIn("data", kwargs)
        self.assertEqual(200, result["status"])

    def test_cancel_payout_transaction(self):
        """PUT cancels a transaction without sending an undocumented payload."""
        self.mock_put({"id": "txn-001"})

        result = self.sdk.payouts().cancel_payout_transaction("batch/001", "txn/001")

        self.mock_http.put.assert_called_once()
        args, kwargs = self.mock_http.put.call_args
        self.assertEqual((), args)
        self.assertEqual(
            "https://api.mercadopago.com/v1/payouts/batch%2F001/transactions/"
            "txn%2F001/cancel", kwargs["url"])
        self.assertIsNone(kwargs["data"])
        self.assertEqual(200, result["status"])

    def test_payouts_factory(self):
        """The public factory shares the SDK transport and request options."""
        resource = self.sdk.payouts()
        self.assertIsInstance(resource, Payouts)
        self.assertIs(self.sdk.request_options, resource.request_options)
        self.assertIs(self.sdk.http_client, self.mock_http)

        options = RequestOptions(access_token="OVERRIDE_TOKEN")
        overridden_resource = self.sdk.payouts(request_options=options)
        self.assertIsInstance(overridden_resource, Payouts)
        self.assertIs(options, overridden_resource.request_options)


if __name__ == "__main__":
    unittest.main()