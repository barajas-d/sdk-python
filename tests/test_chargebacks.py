"""Unit tests for the Chargebacks resource using a mock HTTP client."""
import json
import unittest

from mercadopago.config import RequestOptions
from mercadopago.resources import Chargebacks
from tests.base_client_test import BaseClientTest


class TestChargebacks(BaseClientTest):
    """Test Module: Chargebacks"""


    def test_update_chargeback_escapes_path_id(self):
        payload = {"files": [{"name": "proof.pdf", "description": "Proof",
                              "url": "https://example.com/proof.pdf"}]}
        self.mock_put({"id": "cb/1"})

        result = self.sdk.chargebacks().update_chargeback("cb/1", payload)

        self.mock_http.put.assert_called_once()
        args, kwargs = self.mock_http.put.call_args
        self.assertEqual((), args)
        self.assertEqual("https://api.mercadopago.com/v1/chargebacks/cb%2F1",
                         kwargs["url"])
        self.assertEqual(payload, json.loads(kwargs["data"]))
        self.assertEqual(200, result["status"])

    def test_chargebacks_factory(self):
        resource = self.sdk.chargebacks()
        self.assertIsInstance(resource, Chargebacks)
        self.assertIs(resource.request_options, self.sdk.request_options)

        options = RequestOptions(access_token="another-token")
        overridden = self.sdk.chargebacks(request_options=options)
        self.assertIsInstance(overridden, Chargebacks)
        self.assertIs(overridden.request_options, options)
        self.assertIs(overridden._MPBase__http_client, self.sdk.http_client)


if __name__ == "__main__":
    unittest.main()