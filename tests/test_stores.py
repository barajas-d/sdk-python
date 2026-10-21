"""Unit tests for the Stores resource using a mock HTTP client."""
import json
import unittest

from tests.base_client_test import BaseClientTest


class TestStores(BaseClientTest):
    """Test Module: Stores"""

    def test_get_store(self):
        """GET /stores/{id} sends the ID in the URL without a request body."""
        self.mock_get({"id": "store-123"})

        result = self.sdk.stores().get_store("store-123")

        self.mock_http.get.assert_called_once()
        _, kwargs = self.mock_http.get.call_args
        self.assertEqual("https://api.mercadopago.com/stores/store-123", kwargs["url"])
        self.assertNotIn("data", kwargs)
        self.assertEqual(200, result["status"])

    def test_create_store(self):
        """POST creates a store under the specified user."""
        payload = {"name": "Downtown", "external_id": "branch-1"}
        self.mock_post({"id": "store-123"})

        result = self.sdk.stores().create_store(42, payload)

        self.mock_http.post.assert_called_once()
        _, kwargs = self.mock_http.post.call_args
        self.assertEqual("https://api.mercadopago.com/users/42/stores", kwargs["url"])
        self.assertEqual(payload, json.loads(kwargs["data"]))
        self.assertEqual(201, result["status"])

    def test_search_stores(self):
        """GET sends external_id as a query parameter, not a body."""
        filters = {"external_id": "branch-1"}
        self.mock_get({"results": []})

        result = self.sdk.stores().search_stores(42, filters)

        self.mock_http.get.assert_called_once()
        _, kwargs = self.mock_http.get.call_args
        self.assertEqual("https://api.mercadopago.com/users/42/stores/search", kwargs["url"])
        self.assertEqual(filters, kwargs["params"])
        self.assertNotIn("data", kwargs)
        self.assertEqual(200, result["status"])

    def test_delete_store(self):
        """DELETE addresses a store without sending a body."""
        self.mock_delete(None)

        result = self.sdk.stores().delete_store(42, "store-123")

        self.mock_http.delete.assert_called_once()
        _, kwargs = self.mock_http.delete.call_args
        self.assertEqual("https://api.mercadopago.com/users/42/stores/store-123", kwargs["url"])
        self.assertNotIn("data", kwargs)
        self.assertEqual(204, result["status"])

    def test_update_store(self):
        """PUT updates a store with a JSON payload."""
        payload = {"name": "Uptown"}
        self.mock_put({"id": "store-123"})

        result = self.sdk.stores().update_store(42, "store-123", payload)

        self.mock_http.put.assert_called_once()
        _, kwargs = self.mock_http.put.call_args
        self.assertEqual("https://api.mercadopago.com/users/42/stores/store-123", kwargs["url"])
        self.assertEqual(payload, json.loads(kwargs["data"]))
        self.assertEqual(200, result["status"])


if __name__ == "__main__":
    unittest.main()