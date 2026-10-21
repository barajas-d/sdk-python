"""Unit tests for the CustomerAddress resource using a mock HTTP client."""
import json
import unittest

from mercadopago.resources import CustomerAddress
from tests.base_client_test import BaseClientTest


class TestCustomerAddress(BaseClientTest):
    """Test Module: CustomerAddress"""

    def test_customer_address_factory(self):
        resource = self.sdk.customer_address()
        self.assertIsInstance(resource, CustomerAddress)
        self.assertIs(resource.request_options, self.sdk.request_options)
        self.assertIsInstance(self.sdk.customer_address(), CustomerAddress)

    def test_list_customer_addresses(self):
        self.mock_get({"results": []})

        result = self.sdk.customer_address().list_customer_addresses("customer-1")

        self.mock_http.get.assert_called_once()
        args, kwargs = self.mock_http.get.call_args
        self.assertEqual((), args)
        self.assertEqual(
            "https://api.mercadopago.com/v1/customers/customer-1/addresses",
            kwargs["url"],
        )
        self.assertNotIn("data", kwargs)
        self.assertEqual(200, result["status"])

    def test_create_customer_address(self):
        address = {
            "street_name": "Av. Paulista",
            "street_number": "1000",
            "zip_code": "01310-100",
            "city": "São Paulo",
            "state": "SP",
        }
        self.mock_post({"id": "address-1"})

        result = self.sdk.customer_address().create_customer_address(
            "customer-1", address
        )

        self.mock_http.post.assert_called_once()
        args, kwargs = self.mock_http.post.call_args
        self.assertEqual((), args)
        self.assertEqual(
            "https://api.mercadopago.com/v1/customers/customer-1/addresses",
            kwargs["url"],
        )
        self.assertEqual(address, json.loads(kwargs["data"]))
        self.assertEqual("application/json", kwargs["headers"]["Content-type"])
        self.assertEqual(201, result["status"])

    def test_delete_customer_address(self):
        self.mock_delete({"deleted": True}, status=200)

        result = self.sdk.customer_address().delete_customer_address(
            "customer-1", "address-2"
        )

        self.mock_http.delete.assert_called_once()
        args, kwargs = self.mock_http.delete.call_args
        self.assertEqual((), args)
        self.assertEqual(
            "https://api.mercadopago.com/v1/customers/customer-1/addresses/address-2",
            kwargs["url"],
        )
        self.assertNotIn("data", kwargs)
        self.assertEqual(200, result["status"])

    def test_get_customer_address(self):
        self.mock_get({"id": "address-2"})

        result = self.sdk.customer_address().get_customer_address(
            "customer-1", "address-2"
        )

        self.mock_http.get.assert_called_once()
        args, kwargs = self.mock_http.get.call_args
        self.assertEqual((), args)
        self.assertEqual(
            "https://api.mercadopago.com/v1/customers/customer-1/addresses/address-2",
            kwargs["url"],
        )
        self.assertNotIn("data", kwargs)
        self.assertEqual(200, result["status"])

    def test_update_customer_address(self):
        address = {
            "street_name": "Av. Paulista",
            "street_number": "1000",
            "zip_code": "01310-100",
            "city": "São Paulo",
            "state": "SP",
        }
        self.mock_put({"id": "address-2"})

        result = self.sdk.customer_address().update_customer_address(
            "customer-1", "address-2", address
        )

        self.mock_http.put.assert_called_once()
        args, kwargs = self.mock_http.put.call_args
        self.assertEqual((), args)
        self.assertEqual(
            "https://api.mercadopago.com/v1/customers/customer-1/addresses/address-2",
            kwargs["url"],
        )
        self.assertEqual(address, json.loads(kwargs["data"]))
        self.assertEqual("application/json", kwargs["headers"]["Content-type"])
        self.assertEqual(200, result["status"])


if __name__ == "__main__":
    unittest.main()