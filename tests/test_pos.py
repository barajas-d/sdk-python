"""Unit tests for the POS resource using a mock HTTP client."""
import json
import unittest

from mercadopago.resources import POS
from tests.base_client_test import BaseClientTest


class TestPOS(BaseClientTest):
    """Test Module: POS"""

    def test_list_pos(self):
        """Lists a user's POS using GET without a request body."""
        self.mock_get([{"id": "pos-1"}])

        result = self.sdk.pos().list_pos(12345)

        self.mock_http.get.assert_called_once()
        args, kwargs = self.mock_http.get.call_args
        self.assertEqual((), args)
        self.assertEqual("https://api.mercadopago.com/users/12345/pos", kwargs["url"])
        self.assertNotIn("data", kwargs)
        self.assertEqual(200, result["status"])

    def test_search_pos(self):
        """Searches POS using all documented query filters via SDK.pos()."""
        filters = {
            "external_id": "pos-1",
            "external_store_id": "store-ext-1",
            "store_id": "123",
            "category": 621102,
        }
        self.mock_get({"paging": {}, "results": [{"id": "1"}]})

        resource = self.sdk.pos()
        self.assertIsInstance(resource, POS)
        result = resource.search_pos(filters=filters)

        self.mock_http.get.assert_called_once()
        _, kwargs = self.mock_http.get.call_args
        self.assertEqual("https://api.mercadopago.com/pos", kwargs["url"])
        self.assertEqual(filters, kwargs["params"])
        self.assertEqual(200, result["status"])

    def test_delete_pos(self):
        """Deletes a POS by identifier using SDK.pos()."""
        self.mock_delete(None)

        result = self.sdk.pos().delete_pos("pos-1")

        self.mock_http.delete.assert_called_once()
        args, kwargs = self.mock_http.delete.call_args
        self.assertEqual((), args)
        self.assertEqual("https://api.mercadopago.com/pos/pos-1", kwargs["url"])
        self.assertNotIn("data", kwargs)
        self.assertEqual(204, result["status"])

    def test_delete_pos_escapes_id(self):
        """Escapes identifiers as one path segment without a request body."""
        self.mock_delete(None)

        result = self.sdk.pos().delete_pos("pos/1")

        self.mock_http.delete.assert_called_once()
        args, kwargs = self.mock_http.delete.call_args
        self.assertEqual((), args)
        self.assertEqual("https://api.mercadopago.com/pos/pos%2F1", kwargs["url"])
        self.assertNotIn("data", kwargs)
        self.assertEqual(204, result["status"])

    def test_get_pos(self):
        """Retrieves a POS by identifier without a request body."""
        self.mock_get({"id": "pos-1"})

        result = self.sdk.pos().get_pos("pos-1")

        self.mock_http.get.assert_called_once()
        args, kwargs = self.mock_http.get.call_args
        self.assertEqual((), args)
        self.assertEqual("https://api.mercadopago.com/pos/pos-1", kwargs["url"])
        self.assertNotIn("data", kwargs)
        self.assertEqual(200, result["status"])

    def test_create_pos(self):
        """Creates a POS with a JSON POSRequest via SDK.pos()."""
        payload = {"name": "Main POS", "store_id": "1234567",
                   "external_id": "POS001", "fixed_amount": False}
        self.mock_post({"id": "1"})

        result = self.sdk.pos().create_pos(payload)

        self.mock_http.post.assert_called_once()
        _, kwargs = self.mock_http.post.call_args
        self.assertEqual("https://api.mercadopago.com/pos", kwargs["url"])
        self.assertEqual(payload, json.loads(kwargs["data"]))
        self.assertEqual(201, result["status"])
        self.assertEqual({"id": "1"}, result["response"])

    def test_update_pos(self):
        """Updates a POS by identifier with a JSON POSRequest."""
        payload = {"name": "Updated POS", "store_id": "1234567",
                   "external_id": "POS001", "fixed_amount": False}
        self.mock_put({"id": "pos-1"})

        result = self.sdk.pos().update_pos("pos-1", payload)

        self.mock_http.put.assert_called_once()
        args, kwargs = self.mock_http.put.call_args
        self.assertEqual((), args)
        self.assertEqual("https://api.mercadopago.com/pos/pos-1", kwargs["url"])
        self.assertEqual(payload, json.loads(kwargs["data"]))
        self.assertEqual(200, result["status"])


if __name__ == "__main__":
    unittest.main()