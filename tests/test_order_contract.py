"""Offline wire contract for the nine indexed /v1/orders operations.

Fixtures use OrderRequest -> OrderTransactions -> OrderPayment ->
OrderPaymentMethod, OrderPayer, OrderConfig, OrderItem, OrderShipment,
Order -> OrderTransactionPayment, OrderSearchResult and OrderRefundRequest.
No live credentials or network transport are involved.
"""
import json
import unittest

from mercadopago.config import RequestOptions
from mercadopago.http import HttpClient
from mercadopago.resources.order import Order


class FakeHttpClient(HttpClient):
    """Record the MPBase-to-transport boundary and return a queued envelope."""

    def __init__(self):
        self.calls = []
        self.result = {"status": 200, "response": None}

    def get(self, url, headers, params=None, timeout=None, maxretries=None):
        self.calls.append(("GET", url, {
            "headers": headers, "params": params, "timeout": timeout,
            "maxretries": maxretries,
        }))
        return self.result

    def post(self, url, headers, data=None, params=None, timeout=None, maxretries=None):
        self.calls.append(("POST", url, {
            "headers": headers, "data": data, "params": params,
            "timeout": timeout, "maxretries": maxretries,
        }))
        return self.result

    def put(self, url, headers, data=None, params=None, timeout=None, maxretries=None):
        self.calls.append(("PUT", url, {
            "headers": headers, "data": data, "params": params,
            "timeout": timeout, "maxretries": maxretries,
        }))
        return self.result

    def delete(self, url, headers, params=None, timeout=None, maxretries=None):
        self.calls.append(("DELETE", url, {
            "headers": headers, "params": params, "timeout": timeout,
            "maxretries": maxretries,
        }))
        return self.result


PAYMENT = {
    "amount": "100.00",
    "payment_method": {
        "id": "visa", "type": "credit_card", "token": "card-token",
        "installments": 1, "statement_descriptor": "STORE",
    },
    "expiration_time": "P1D",
    "date_of_expiration": "2027-01-01T00:00:00Z",
}
ORDER_REQUEST = {
    "type": "online", "processing_mode": "automatic", "total_amount": "100.00",
    "payer": {
        "email": "buyer@example.com", "first_name": "Alex", "last_name": "Buyer",
        "identification": {"type": "CPF", "number": "99999999999"},
        "phone": {"area_code": "11", "number": "43434343"},
        "address": {"zip_code": "11034430", "street_name": "Main",
                    "street_number": "100", "city": "Sao Paulo", "state": "SP"},
    },
    "transactions": {"payments": [PAYMENT]},
    "items": [{"title": "Item", "quantity": 1, "unit_price": 100.0,
               "category_id": "goods"}],
    "shipment": {"mode": "custom", "cost": "10.00",
                 "address": {"zip_code": "11034430", "street_name": "Main",
                             "street_number": "100"}},
    "config": {"online": {"transaction_security": {
        "validation": "required", "liability_shift": "required",
    }, "callback_url": "https://merchant.example/return"}},
    "integration_data": {"platform_id": "platform-1", "sponsor_id": 123},
}
ORDER_RESPONSE = {
    "id": "ORD-1", "type": "online", "status": "processed",
    "status_detail": "accredited", "total_amount": "100.00",
    "payer": ORDER_REQUEST["payer"], "shipment": ORDER_REQUEST["shipment"],
    "items": ORDER_REQUEST["items"], "config": ORDER_REQUEST["config"],
    "integration_data": ORDER_REQUEST["integration_data"],
    "transactions": {"payments": [{
        "id": "PAY-1", "amount": "100.00", "status": "processed",
        "status_detail": "accredited",
        "payment_method": {"id": "visa", "type": "credit_card"},
    }]},
}
BASE_URL = "https://api.mercadopago.com/v1/orders"


class TestOrderContract(unittest.TestCase):
    """Verify the public Order API against the actual serialized HTTP calls."""

    def setUp(self):
        self.client = FakeHttpClient()
        self.order = Order(RequestOptions(access_token="offline-token"), self.client)

    def assert_call(self, verb, suffix, options=None):
        actual_verb, url, kwargs = self.client.calls[-1]
        self.assertEqual((actual_verb, url), (verb, BASE_URL + suffix))
        self.assertEqual(kwargs["headers"]["Authorization"], "Bearer offline-token")
        if options is None:
            self.assertEqual(kwargs["timeout"], 60.0)
            self.assertEqual(kwargs["maxretries"], 3)
        else:
            self.assertEqual(kwargs["timeout"], options.connection_timeout)
            self.assertEqual(kwargs["maxretries"], options.max_retries)
            self.assertEqual(kwargs["headers"]["x-idempotency-key"],
                             "123e4567-e89b-42d3-a456-426614174000")
            self.assertEqual(kwargs["headers"]["x-test"], "forwarded")
        return kwargs

    @staticmethod
    def options():
        return RequestOptions(
            connection_timeout=5.0, max_retries=1,
            custom_headers={"x-idempotency-key": "123e4567-e89b-42d3-a456-426614174000",
                            "x-test": "forwarded"},
        )

    def test_create_serializes_complete_nested_request_and_preserves_response(self):
        self.client.result = {"status": 201, "response": ORDER_RESPONSE}
        options = self.options()
        result = self.order.create(ORDER_REQUEST, request_options=options)
        call = self.assert_call("POST", "", options)
        self.assertIsNone(call["params"])
        self.assertEqual(json.loads(call["data"]), ORDER_REQUEST)
        self.assertEqual(call["headers"]["Content-type"], "application/json")
        self.assertEqual(result, {"status": 201, "response": ORDER_RESPONSE})
        self.assertEqual(result["response"]["payer"]["identification"]["number"],
                         "99999999999")
        self.assertEqual(result["response"]["shipment"]["address"]["zip_code"],
                         "11034430")
        self.assertEqual(result["response"]["config"]["online"]["callback_url"],
                         "https://merchant.example/return")
        self.assertEqual(result["response"]["integration_data"]["sponsor_id"], 123)
        self.assertEqual(result["response"]["transactions"]["payments"][0]
                         ["payment_method"]["id"], "visa")

    def test_get_order_keeps_nested_envelope(self):
        self.client.result = {"status": 200, "response": ORDER_RESPONSE}
        result = self.order.get("ORD-1", request_options=self.options())
        call = self.assert_call("GET", "/ORD-1", self.options())
        self.assertIsNone(call["params"])
        self.assertEqual(result, {"status": 200, "response": ORDER_RESPONSE})
        self.assertEqual(result["response"]["items"][0]["title"], "Item")
        self.assertEqual(result["response"]["transactions"]["payments"][0]["id"],
                         "PAY-1")

    def test_search_forwards_date_range_filters_and_pagination(self):
        filters = {
            "begin_date": "2026-01-01T00:00:00Z",
            "end_date": "2026-02-01T00:00:00Z",
            "external_reference": "reference-1", "type": "online",
            "status": "processed", "limit": 10, "offset": 20,
        }
        search_result = {"data": [ORDER_RESPONSE], "paging": {
            "total": 1, "limit": 10, "offset": 20,
        }}
        self.client.result = {"status": 200, "response": search_result}
        options = self.options()
        result = self.order.search(filters=filters, request_options=options)
        call = self.assert_call("GET", "", options)
        self.assertEqual(call["params"], filters)
        self.assertEqual(result, {"status": 200, "response": search_result})
        self.assertEqual(result["response"]["data"][0]["payer"]["phone"]["number"],
                         "43434343")
        self.assertEqual(result["response"]["paging"]["offset"], 20)

    def test_cancel_capture_and_process_routes_and_responses(self):
        for method, action in ((self.order.cancel, "cancel"),
                               (self.order.capture, "capture"),
                               (self.order.process, "process")):
            with self.subTest(action=action):
                body = dict(ORDER_RESPONSE, status="canceled" if action == "cancel"
                            else "processed")
                self.client.result = {"status": 200, "response": body}
                options = self.options()
                result = method("ORD-1", request_options=options)
                call = self.assert_call("POST", "/ORD-1/" + action, options)
                self.assertIsNone(call["data"])
                self.assertIsNone(call["params"])
                self.assertEqual(result, {"status": 200, "response": body})
                self.assertEqual(result["response"]["transactions"]["payments"][0]
                                 ["payment_method"]["type"], "credit_card")

    def test_add_transaction_serializes_payment_details_and_returns_payments(self):
        payload = {"payments": [PAYMENT]}
        payments = {"payments": ORDER_RESPONSE["transactions"]["payments"]}
        self.client.result = {"status": 201, "response": payments}
        options = self.options()
        result = self.order.create_transaction("ORD-1", payload, request_options=options)
        call = self.assert_call("POST", "/ORD-1/transactions", options)
        self.assertEqual(json.loads(call["data"]), payload)
        self.assertEqual(json.loads(call["data"])["payments"][0]["date_of_expiration"],
                         "2027-01-01T00:00:00Z")
        self.assertEqual(result, {"status": 201, "response": payments})
        self.assertEqual(result["response"]["payments"][0]["status_detail"],
                         "accredited")
        self.assertEqual(result["response"]["payments"][0]["payment_method"]["id"],
                         "visa")

    def test_partial_and_full_refund_preserve_response_and_empty_body_semantics(self):
        body = {"id": "REF-1", "status": "processed", "status_detail": "accredited",
                "transactions": {"payments": [{"id": "PAY-1", "amount": "25.00"}]}}
        self.client.result = {"status": 201, "response": body}
        partial = {"transactions": [{"id": "PAY-1", "amount": "25.00"}]}
        options = self.options()
        result = self.order.refund("ORD-1", partial, request_options=options)
        call = self.assert_call("POST", "/ORD-1/refund", options)
        self.assertEqual(json.loads(call["data"]), partial)
        self.assertEqual(result, {"status": 201, "response": body})
        self.assertEqual(result["response"]["transactions"]["payments"][0]["amount"],
                         "25.00")
        self.assertEqual(result["response"]["status_detail"], "accredited")
        full = self.order.refund_transaction("ORD-2", request_options=options)
        call = self.assert_call("POST", "/ORD-2/refund", options)
        self.assertIsNone(call["data"])
        self.assertIsNone(call["params"])
        self.assertEqual(full, {"status": 201, "response": body})

    def test_delete_transaction_204_no_content(self):
        self.client.result = {"status": 204, "response": None}
        options = self.options()
        result = self.order.delete_transaction("ORD-1", "PAY-2", request_options=options)
        call = self.assert_call("DELETE", "/ORD-1/transactions/PAY-2", options)
        self.assertIsNone(call["params"])
        self.assertEqual(result, {"status": 204, "response": None})


class TestOrderUuidIdempotency(unittest.TestCase):
    """Exercise caller-supplied UUID idempotency keys on write operations."""

    IDEMPOTENCY_KEY = "123e4567-e89b-42d3-a456-426614174000"

    def setUp(self):
        self.client = FakeHttpClient()
        self.order = Order(RequestOptions(access_token="offline-token"), self.client)
        self.options = RequestOptions(
            connection_timeout=5.0, max_retries=1,
            custom_headers={"x-idempotency-key": self.IDEMPOTENCY_KEY,
                            "x-test": "forwarded"},
        )

    def assert_forwarded(self, verb, suffix):
        actual_verb, url, kwargs = self.client.calls[-1]
        self.assertEqual((actual_verb, url), (verb, BASE_URL + suffix))
        self.assertEqual(kwargs["headers"]["Authorization"], "Bearer offline-token")
        self.assertEqual(kwargs["headers"]["x-idempotency-key"],
                         self.IDEMPOTENCY_KEY)
        self.assertEqual(kwargs["headers"]["x-test"], "forwarded")
        self.assertEqual(kwargs["timeout"], 5.0)
        self.assertEqual(kwargs["maxretries"], 1)
        return kwargs

    def test_update_transaction_serializes_payment_method_and_preserves_response(self):
        payload = {"payment_method": dict(PAYMENT["payment_method"])}
        payment = ORDER_RESPONSE["transactions"]["payments"][0]
        self.client.result = {"status": 200, "response": payment}
        result = self.order.update_transaction(
            "ORD-1", "PAY-1", payload, request_options=self.options,
        )
        call = self.assert_forwarded("PUT", "/ORD-1/transactions/PAY-1")
        self.assertEqual(json.loads(call["data"]), payload)
        self.assertIsNone(call["params"])
        self.assertEqual(call["headers"]["Content-type"], "application/json")
        self.assertEqual(result, {"status": 200, "response": payment})
        self.assertEqual(result["response"]["payment_method"]["id"], "visa")
        self.assertEqual(result["response"]["status_detail"], "accredited")

    def test_post_operations_forward_caller_supplied_uuid(self):
        cases = (
            (lambda: self.order.create(ORDER_REQUEST, request_options=self.options), ""),
            (lambda: self.order.cancel("ORD-1", request_options=self.options),
             "/ORD-1/cancel"),
            (lambda: self.order.capture("ORD-1", request_options=self.options),
             "/ORD-1/capture"),
            (lambda: self.order.process("ORD-1", request_options=self.options),
             "/ORD-1/process"),
            (lambda: self.order.refund("ORD-1", request_options=self.options),
             "/ORD-1/refund"),
            (lambda: self.order.create_transaction(
                "ORD-1", {"payments": [PAYMENT]}, request_options=self.options),
             "/ORD-1/transactions"),
        )
        for invoke, suffix in cases:
            with self.subTest(suffix=suffix):
                invoke()
                self.assert_forwarded("POST", suffix)


if __name__ == "__main__":
    unittest.main()
