"""Unit tests for the CustomerAddress resource using a mock HTTP client."""
import json
import unittest

from tests.base_client_test import BaseClientTest


class TestCustomerAddress(BaseClientTest):
    """Test Module: CustomerAddress."""

    def test_list_customer_addresses(self):
        self.mock_get([{"id": "addr-1"}])

        result = self.sdk.customer_address().list_customer_addresses("cust-1")

        self.mock_http.get.assert_called_once()
        _, kwargs = self.mock_http.get.call_args
        self.assertEqual("https://api.mercadopago.com/v1/customers/cust-1/addresses", kwargs["url"])
        self.assertIsNone(kwargs["params"])
        self.assertEqual(200, result["status"])

    def test_create_customer_address(self):
        address_object = {"zip_code": "01310-100", "street_name": "Av. Paulista",
                          "street_number": "1000", "city": "São Paulo", "state": "SP"}
        self.mock_post({"id": "addr-1"})

        result = self.sdk.customer_address().create_customer_address("cust-1", address_object)

        self.mock_http.post.assert_called_once()
        _, kwargs = self.mock_http.post.call_args
        self.assertEqual("https://api.mercadopago.com/v1/customers/cust-1/addresses", kwargs["url"])
        self.assertEqual(address_object, json.loads(kwargs["data"]))
        self.assertEqual(201, result["status"])

    def test_delete_customer_address(self):
        self.mock_delete(None)

        result = self.sdk.customer_address().delete_customer_address("cust-1", "addr-1")

        self.mock_http.delete.assert_called_once()
        _, kwargs = self.mock_http.delete.call_args
        self.assertEqual("https://api.mercadopago.com/v1/customers/cust-1/addresses/addr-1", kwargs["url"])
        self.assertIsNone(kwargs["params"])
        self.assertEqual(204, result["status"])

    def test_get_customer_address(self):
        self.mock_get({"id": "addr-1"})

        result = self.sdk.customer_address().get_customer_address("cust-1", "addr-1")

        self.mock_http.get.assert_called_once()
        _, kwargs = self.mock_http.get.call_args
        self.assertEqual("https://api.mercadopago.com/v1/customers/cust-1/addresses/addr-1", kwargs["url"])
        self.assertIsNone(kwargs["params"])
        self.assertEqual(200, result["status"])

    def test_update_customer_address(self):
        address_object = {"zip_code": "01310-100", "street_name": "Av. Paulista",
                          "street_number": "1000", "city": "São Paulo", "state": "SP"}
        self.mock_put({"id": "addr-1"})

        result = self.sdk.customer_address().update_customer_address(
            "cust-1", "addr-1", address_object)

        self.mock_http.put.assert_called_once()
        _, kwargs = self.mock_http.put.call_args
        self.assertEqual("https://api.mercadopago.com/v1/customers/cust-1/addresses/addr-1", kwargs["url"])
        self.assertEqual(address_object, json.loads(kwargs["data"]))
        self.assertEqual(200, result["status"])


if __name__ == "__main__":
    unittest.main()