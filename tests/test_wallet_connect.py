"""Unit tests for the WalletConnect resource using a mock HTTP client."""
import json
import unittest

from mercadopago.config.request_options import RequestOptions
from mercadopago.resources import WalletConnect
from tests.base_client_test import BaseClientTest


class TestWalletConnect(BaseClientTest):
    """Test Module: WalletConnect"""

    def test_get_wallet_agreement(self):
        """GET sends the agreement ID, optional query and platform header only."""
        options = RequestOptions(platform_id="platform-1")
        self.mock_get({"id": "agreement-1"})

        result = self.sdk.wallet_connect().get_wallet_agreement(
            "agreement-1", params={"client.id": "client-1"},
            request_options=options)

        self.mock_http.get.assert_called_once()
        args, kwargs = self.mock_http.get.call_args
        self.assertEqual((), args)
        self.assertEqual(
            "https://api.mercadopago.com/v2/wallet_connect/agreements/agreement-1",
            kwargs["url"])
        self.assertEqual({"client.id": "client-1"}, kwargs["params"])
        self.assertEqual("platform-1", kwargs["headers"]["x-platform-id"])
        self.assertNotIn("data", kwargs)
        self.assertEqual(200, result["status"])

    def test_delete_wallet_agreement(self):
        """DELETE revokes the agreement with optional query and platform header."""
        options = RequestOptions(platform_id="platform-1")
        self.mock_delete({"id": "agreement-1"}, status=200)

        result = self.sdk.wallet_connect().delete_wallet_agreement(
            "agreement-1", params={"client.id": "client-1"},
            request_options=options)

        self.mock_http.delete.assert_called_once()
        args, kwargs = self.mock_http.delete.call_args
        self.assertEqual((), args)
        self.assertEqual(
            "https://api.mercadopago.com/v2/wallet_connect/agreements/agreement-1",
            kwargs["url"])
        self.assertEqual({"client.id": "client-1"}, kwargs["params"])
        self.assertEqual("platform-1", kwargs["headers"]["x-platform-id"])
        self.assertNotIn("data", kwargs)
        self.assertEqual(200, result["status"])

    def test_create_wallet_agreement(self):
        """Agreement fields are JSON; client.id and platform ID are not."""
        payload = {
            "return_uri": "https://example.com/return",
            "external_flow_id": "flow-1",
        }
        options = RequestOptions(platform_id="platform-1")
        self.mock_post({"agreement_id": "agreement-1"}, status=200)

        result = self.sdk.wallet_connect().create_wallet_agreement(
            payload, params={"client.id": "client-1"}, request_options=options)

        self.mock_http.post.assert_called_once()
        args, kwargs = self.mock_http.post.call_args
        self.assertEqual((), args)
        self.assertEqual("https://api.mercadopago.com/v2/wallet_connect/agreements",
                         kwargs["url"])
        self.assertEqual(payload, json.loads(kwargs["data"]))
        self.assertEqual({"client.id": "client-1"}, kwargs["params"])
        self.assertEqual("platform-1", kwargs["headers"]["x-platform-id"])
        self.assertEqual(200, result["status"])

    def test_create_wallet_payer_token(self):
        """The authorization code is sent in the body, not the response token."""
        payload = {"code": "authorization-code"}
        self.mock_post({"payer_token": "payer-token"}, status=200)

        result = self.sdk.wallet_connect().create_wallet_payer_token(
            "agreement-1", payload)

        self.mock_http.post.assert_called_once()
        args, kwargs = self.mock_http.post.call_args
        self.assertEqual((), args)
        self.assertEqual(
            "https://api.mercadopago.com/v2/wallet_connect/agreements/"
            "agreement-1/payer_token", kwargs["url"])
        self.assertEqual(payload, json.loads(kwargs["data"]))
        self.assertEqual(200, result["status"])

    def test_validate_wallet_coupon(self):
        """The coupon ID is JSON and the payer token is a header."""
        payload = {"id": "coupon-1"}
        options = RequestOptions(custom_headers={"x-payer-token": "payer-token"})
        self.mock_post({"status": "active"}, status=200)

        result = self.sdk.wallet_connect().validate_wallet_coupon(
            payload, "payer-token", request_options=options)

        self.mock_http.post.assert_called_once()
        args, kwargs = self.mock_http.post.call_args
        self.assertEqual((), args)
        self.assertEqual("https://api.mercadopago.com/v2/wallet_connect/coupons",
                         kwargs["url"])
        self.assertEqual(payload, json.loads(kwargs["data"]))
        self.assertEqual("payer-token", kwargs["headers"]["x-payer-token"])
        self.assertEqual(200, result["status"])

    def test_create_wallet_discount(self):
        """The discount fields are JSON and the payer token is a header."""
        payload = {"coupon": "coupon-1", "amount": 100.0}
        options = RequestOptions(custom_headers={"x-payer-token": "payer-token"})
        self.mock_post({"discount": {"amount": 10.0}}, status=200)

        result = self.sdk.wallet_connect().create_wallet_discount(
            payload, request_options=options)

        self.mock_http.post.assert_called_once()
        args, kwargs = self.mock_http.post.call_args
        self.assertEqual((), args)
        self.assertEqual("https://api.mercadopago.com/v2/wallet_connect/discounts",
                         kwargs["url"])
        self.assertEqual(payload, json.loads(kwargs["data"]))
        self.assertEqual("payer-token", kwargs["headers"]["x-payer-token"])
        self.assertEqual(200, result["status"])

    def test_get_wallet_agreement_without_optional_parameters(self):
        """GET escapes the agreement ID without adding a body or query."""
        self.mock_get({"id": "agreement/1"})

        result = self.sdk.wallet_connect().get_wallet_agreement("agreement/1")

        self.mock_http.get.assert_called_once()
        args, kwargs = self.mock_http.get.call_args
        self.assertEqual((), args)
        self.assertEqual(
            "https://api.mercadopago.com/v2/wallet_connect/agreements/agreement%2F1",
            kwargs["url"])
        self.assertIsNone(kwargs["params"])
        self.assertNotIn("data", kwargs)
        self.assertEqual(200, result["status"])

    def test_wallet_connect_factory(self):
        """The public factory binds the SDK client and configured options."""
        options = RequestOptions(platform_id="platform-1")

        resource = self.sdk.wallet_connect(options)

        self.assertIsInstance(resource, WalletConnect)
        self.assertIs(options, resource.request_options)
        self.assertIs(self.sdk.http_client, self.mock_http)


if __name__ == "__main__":
    unittest.main()