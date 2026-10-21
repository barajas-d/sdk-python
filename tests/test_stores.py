"""Unit tests for the Stores resource using a mock HTTP client."""
import json
import unittest

from mercadopago.config import RequestOptions
from tests.base_client_test import BaseClientTest


class TestStores(BaseClientTest):
    """Test Module: Stores"""

    def test_get_store(self):
        """Retrieves a store by path ID without sending a request body."""
        fixture = {"id": "store-1"}
        self.mock_get(fixture)
        options = RequestOptions(
            access_token="store-token", custom_headers={"X-Store-Test": "enabled"}
        )

        result = self.sdk.stores().get_store("store-1", request_options=options)

        self.mock_http.get.assert_called_once()
        args, kwargs = self.mock_http.get.call_args
        self.assertEqual((), args)
        self.assertEqual("https://api.mercadopago.com/stores/store-1", kwargs["url"])
        self.assertIsNone(kwargs["params"])
        self.assertNotIn("data", kwargs)
        self.assertEqual("Bearer store-token", kwargs["headers"]["Authorization"])
        self.assertEqual("enabled", kwargs["headers"]["X-Store-Test"])
        self.assertEqual(200, result["status"])
        self.assertEqual(fixture, result["response"])

    def test_create_store(self):
        """Posts store data to the user's stores collection."""
        fixture = {"id": "store-1"}
        payload = {"name": "Main", "external_id": "ext-1",
                   "location": {"street_name": "Main Street"},
                   "business_hours": {"monday": []}}
        self.mock_post(fixture)

        result = self.sdk.stores().create_store(123, payload)

        self.mock_http.post.assert_called_once()
        args, kwargs = self.mock_http.post.call_args
        self.assertEqual((), args)
        self.assertEqual("https://api.mercadopago.com/users/123/stores", kwargs["url"])
        self.assertEqual(payload, json.loads(kwargs["data"]))
        self.assertEqual(201, result["status"])

    def test_search_stores(self):
        """Searches stores with the optional external ID as a query filter."""
        fixture = {"results": []}
        self.mock_get(fixture)

        result = self.sdk.stores().search_stores(123, external_id="ext-1")

        self.mock_http.get.assert_called_once()
        args, kwargs = self.mock_http.get.call_args
        self.assertEqual((), args)
        self.assertEqual("https://api.mercadopago.com/users/123/stores/search",
                         kwargs["url"])
        self.assertEqual({"external_id": "ext-1"}, kwargs["params"])
        self.assertEqual(200, result["status"])

    def test_delete_store(self):
        """Deletes a store without sending a body."""
        self.mock_delete(None, status=200)

        result = self.sdk.stores().delete_store(123, "store-1")

        self.mock_http.delete.assert_called_once()
        args, kwargs = self.mock_http.delete.call_args
        self.assertEqual((), args)
        self.assertEqual("https://api.mercadopago.com/users/123/stores/store-1",
                         kwargs["url"])
        self.assertIsNone(kwargs["params"])
        self.assertNotIn("data", kwargs)
        self.assertEqual(200, result["status"])

    def test_update_store(self):
        """Puts a StoreRequest JSON body to the user's store."""
        fixture = {"id": "store-1", "name": "Updated"}
        payload = {"name": "Updated", "external_id": "ext-2"}
        self.mock_put(fixture)

        result = self.sdk.stores().update_store(123, "store-1", payload)

        self.mock_http.put.assert_called_once()
        args, kwargs = self.mock_http.put.call_args
        self.assertEqual((), args)
        self.assertEqual("https://api.mercadopago.com/users/123/stores/store-1",
                         kwargs["url"])
        self.assertEqual(payload, json.loads(kwargs["data"]))
        self.assertEqual(200, result["status"])


if __name__ == "__main__":
    unittest.main()