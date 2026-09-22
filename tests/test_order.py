"""Local contract tests for the Orders API resource."""
import json
import unittest

from mercadopago.config import RequestOptions
from mercadopago.http import HttpClient
from mercadopago.resources.order import Order


class FakeHttpClient(HttpClient):
    """Records requests and returns configured responses without network I/O."""

    def __init__(self):
        self.calls = []
        self.response = {"status": 200, "response": {"id": "ORD123"}}

    def _record(self, method, url, headers, data=None, params=None, **kwargs):
        self.calls.append({"method": method, "url": url, "headers": headers,
                           "data": data, "params": params, **kwargs})
        return self.response

    def get(self, url, headers, params=None, **kwargs):
        return self._record("GET", url, headers, params=params, **kwargs)

    def post(self, url, headers, data=None, params=None, **kwargs):
        return self._record("POST", url, headers, data=data, params=params, **kwargs)

    def put(self, url, headers, data=None, params=None, **kwargs):
        return self._record("PUT", url, headers, data=data, params=params, **kwargs)

    def delete(self, url, headers, params=None, **kwargs):
        return self._record("DELETE", url, headers, params=params, **kwargs)


class TestOrder(unittest.TestCase):
    """Verifies the public Order operations against ``/v1/orders*``."""

    def setUp(self):
        self.http = FakeHttpClient()
        options = RequestOptions(
            access_token="TEST_ACCESS_TOKEN",
            custom_headers={"x-idempotency-key": "fixed-key"},
        )
        self.order = Order(options, self.http)

    def assert_call(self, method, path, body=None):
        call = self.http.calls[-1]
        self.assertEqual(call["method"], method)
        self.assertEqual(call["url"], "https://api.mercadopago.com" + path)
        if body is not None:
            self.assertEqual(json.loads(call["data"]), body)
        return call

    def test_search_create_and_get(self):
        filters = {"begin_date": "2025-01-01T00:00:00Z",
                   "end_date": "2025-01-31T23:59:59Z", "limit": 30}
        self.order.search(filters)
        self.assertEqual(self.assert_call("GET", "/v1/orders")["params"], filters)

        body = {"type": "online", "total_amount": "100.00",
                "payer": {"email": "customer@example.com"},
                "transactions": {"payments": []}}
        self.http.response = {"status": 201, "response": {"id": "ORD123"}}
        self.assertEqual(self.order.create(body)["status"], 201)
        call = self.assert_call("POST", "/v1/orders", body)
        self.assertEqual(call["headers"]["x-idempotency-key"], "fixed-key")

        self.http.response = {"status": 200, "response": {"id": "ORD123"}}
        self.assertEqual(self.order.get("ORD123")["status"], 200)
        self.assert_call("GET", "/v1/orders/ORD123")

    def test_order_actions_use_post_and_idempotency(self):
        for operation, suffix in ((self.order.process, "process"),
                                  (self.order.cancel, "cancel"),
                                  (self.order.capture, "capture")):
            operation("ORD123")
            call = self.assert_call("POST", f"/v1/orders/ORD123/{suffix}")
            self.assertEqual(call["headers"]["x-idempotency-key"], "fixed-key")

    def test_transaction_operations(self):
        create_body = {"payments": [{"amount": "100.00", "payment_method": {
            "id": "visa", "type": "credit_card"}}]}
        self.http.response = {"status": 201, "response": {"payments": []}}
        self.assertEqual(self.order.create_transaction("ORD123", create_body)["status"], 201)
        self.assert_call("POST", "/v1/orders/ORD123/transactions", create_body)

        update_body = {"payment_method": {"id": "master", "type": "credit_card"}}
        self.http.response = {"status": 200, "response": {"id": "TX123"}}
        self.assertEqual(self.order.update_transaction(
            "ORD123", "TX123", update_body)["status"], 200)
        self.assert_call("PUT", "/v1/orders/ORD123/transactions/TX123", update_body)

        self.http.response = {"status": 204, "response": None}
        self.assertEqual(self.order.delete_transaction("ORD123", "TX123")["status"], 204)
        self.assert_call("DELETE", "/v1/orders/ORD123/transactions/TX123")

    def test_refund_supports_partial_and_omitted_full_body(self):
        partial = {"transactions": [{"id": "TX123", "amount": "25.00"}]}
        self.http.response = {"status": 201, "response": {"id": "REF123"}}
        self.assertEqual(self.order.refund("ORD123", partial)["status"], 201)
        self.assert_call("POST", "/v1/orders/ORD123/refund", partial)

        self.order.refund("ORD123")
        call = self.assert_call("POST", "/v1/orders/ORD123/refund")
        self.assertIsNone(call["data"])

    def test_search_requires_date_filters_and_bodies_are_dicts(self):
        for filters in (None, {}, {"begin_date": "2025-01-01T00:00:00Z"}):
            with self.subTest(filters=filters), self.assertRaises(ValueError):
                self.order.search(filters)
        for operation, args in (
                (self.order.create, ([],)),
                (self.order.create_transaction, ("ORD123", [])),
                (self.order.update_transaction, ("ORD123", "TX123", [])),
                (self.order.refund, ("ORD123", []))):
            with self.assertRaises(ValueError):
                operation(*args)

    def test_api_errors_are_returned_without_reinterpretation(self):
        operations = (
            (self.order.search, ({"begin_date": "a", "end_date": "b"},)),
            (self.order.create, ({},)), (self.order.get, ("ORD123",)),
            (self.order.process, ("ORD123",)), (self.order.cancel, ("ORD123",)),
            (self.order.capture, ("ORD123",)),
            (self.order.create_transaction, ("ORD123", {"payments": []})),
        )
        for (operation, args), status in zip(
                operations, (400, 401, 404, 409, 422, 423, 500)):
            expected = {"status": status, "response": {"error": "api_error"}}
            self.http.response = expected
            self.assertIs(operation(*args), expected)


if __name__ == "__main__":
    unittest.main()