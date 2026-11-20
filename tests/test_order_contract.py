"""Offline wire contract for the Orders resource (no API credentials required)."""
import json
import unittest

from mercadopago import SDK
from mercadopago.config import RequestOptions
from mercadopago.http import HttpClient
from mercadopago.resources.order import Order
from mercadopago.core import MPBase


class FakeHttpClient(HttpClient):
    """Record SDK transport calls and return caller-supplied API responses."""

    def __init__(self):
        self.calls = []
        self.result = None

    def _record(self, method, **kwargs):
        self.calls.append((method, kwargs))
        return self.result

    def get(self, url, headers, params=None, timeout=None, maxretries=None):
        return self._record("GET", url=url, headers=headers, params=params,
                            timeout=timeout, maxretries=maxretries)

    def post(self, url, headers, data=None, params=None, timeout=None, maxretries=None):
        return self._record("POST", url=url, headers=headers, data=data,
                            params=params, timeout=timeout, maxretries=maxretries)

    def put(self, url, headers, data=None, params=None, timeout=None, maxretries=None):
        return self._record("PUT", url=url, headers=headers, data=data,
                            params=params, timeout=timeout, maxretries=maxretries)

    def delete(self, url, headers, params=None, timeout=None, maxretries=None):
        return self._record("DELETE", url=url, headers=headers, params=params,
                            timeout=timeout, maxretries=maxretries)


class TestOrderContract(unittest.TestCase):
    """Assert the actual Order/MPBase JSON and response-wrapper behavior."""

    BASE = "https://api.mercadopago.com/v1/orders"
    ORDER_ID = "ORD-abc123"
    PAYMENT_ID = "PAY-def456"
    IDEMPOTENCY_KEY = "123e4567-e89b-42d3-a456-426614174000"

    def setUp(self):
        self.http = FakeHttpClient()
        self.order = SDK("TEST_ACCESS_TOKEN", http_client=self.http).order()
        self.assertIsInstance(self.order, Order)
        self.assertIsInstance(self.order, MPBase)
        self.options = RequestOptions(custom_headers={
            "x-idempotency-key": self.IDEMPOTENCY_KEY,
        })

    def respond(self, method, path, payload, status=200, options=None, body=None):
        """Check a single transport call, including unchanged SDK wrapper."""
        self.http.calls.clear()
        self.http.result = {"status": status, "response": payload}
        result = method()
        self.assertEqual(result, self.http.result)
        self.assertIs(result["response"], payload)
        self.assertEqual(len(self.http.calls), 1)
        verb, call = self.http.calls[0]
        self.assertEqual(verb, path[0])
        self.assertEqual(call["url"], self.BASE + path[1])
        self.assertEqual(call["headers"]["Authorization"], "Bearer TEST_ACCESS_TOKEN")
        if options:
            self.assertEqual(call["headers"]["x-idempotency-key"], self.IDEMPOTENCY_KEY)
        if body is not None:
            self.assertEqual(json.loads(call["data"]), body)
            self.assertEqual(call["headers"]["Content-type"], "application/json")
        return call

    @staticmethod
    def payment_method():
        return {"id": "visa", "type": "credit_card", "token": "card-token",
                "installments": 2}

    def order_body(self):
        return {
            "type": "online", "processing_mode": "automatic",
            "total_amount": "120.00", "external_reference": "checkout-123",
            "payer": {"email": "buyer@example.com", "first_name": "Ana",
                      "last_name": "Silva", "identification": {"type": "CPF",
                                                              "number": "12345678909"},
                      "phone": {"area_code": "11", "number": "999998888"}},
            "transactions": {"payments": [{"amount": "120.00",
                                            "payment_method": self.payment_method()}]},
            "items": [{"title": "Notebook", "quantity": 1, "unit_price": 120.00,
                       "category_id": "electronics"}],
            "shipment": {"address": {"zip_code": "01310-100",
                                     "street_name": "Av. Paulista",
                                     "street_number": "1000"}},
            "config": {"online": {"transaction_security": {
                                      "validation": "supported",
                                      "liability_shift": "required"},
                                  "callback_url": "https://example.com/callback"}},
            "integration_data": {"sponsor_id": 123,
                                 "platform_id": "platform-1"},
            "additional_info": {"payer": {"ip_address": "200.100.50.25"}},
        }

    def order_response(self):
        return {"id": self.ORDER_ID, "status": "created", "type": "online",
                "payer": self.order_body()["payer"],
                "items": self.order_body()["items"],
                "shipment": self.order_body()["shipment"],
                "config": self.order_body()["config"],
                "transactions": {"payments": [
                    {"id": self.PAYMENT_ID, "amount": "120.00",
                     "payment_method": self.payment_method()}]}}

    def test_create_serializes_nested_order_request_and_returns_order(self):
        body = self.order_body()
        response = self.order_response()
        self.respond(lambda: self.order.create(body, request_options=self.options),
                     ("POST", ""), response, status=201, options=True, body=body)

    def test_search_forwards_required_dates_without_optional_filters(self):
        filters = {"begin_date": "2026-01-01T00:00:00Z",
                   "end_date": "2026-01-02T00:00:00Z"}
        response = {"data": [self.order_response()]}
        call = self.respond(lambda: self.order.search(filters),
                            ("GET", ""), response)
        self.assertEqual(call["params"], filters)
        self.assertEqual(call["params"]["end_date"], "2026-01-02T00:00:00Z")
        self.assertEqual(response["data"][0]["payer"]["identification"]["type"], "CPF")
        self.assertEqual(response["data"][0]["config"]["online"]["callback_url"],
                         "https://example.com/callback")

    def test_search_forwards_all_documented_query_keys_and_nested_results(self):
        filters = {"begin_date": "2026-01-01T00:00:00Z",
                   "end_date": "2026-01-02T00:00:00Z",
                   "external_reference": "checkout-123", "type": "online",
                   "status": "created", "limit": 15, "offset": 5}
        response = {"data": [self.order_response()],
                    "paging": {"total": 1, "limit": 15, "offset": 5}}
        call = self.respond(lambda: self.order.search(filters, self.options),
                            ("GET", ""), response, options=True)
        self.assertEqual(call["params"], filters)
        self.assertEqual(call["params"]["limit"], 15)

    def test_get_process_cancel_preserve_nested_order(self):
        response = self.order_response()
        self.respond(lambda: self.order.get(self.ORDER_ID),
                     ("GET", "/" + self.ORDER_ID), response)
        for action in ("process", "cancel"):
            with self.subTest(action=action):
                self.respond(lambda: getattr(self.order, action)(
                    self.ORDER_ID, request_options=self.options),
                    ("POST", "/" + self.ORDER_ID + "/" + action),
                    response, options=True)

    def test_capture_only_assumes_inline_response_fields(self):
        response = {"id": self.ORDER_ID, "status": "processed",
                    "status_detail": "captured", "transactions": {}}
        self.respond(lambda: self.order.capture(self.ORDER_ID, self.options),
                     ("POST", "/" + self.ORDER_ID + "/capture"),
                     response, options=True)

    def test_add_transaction_forwards_payment_and_retains_payment_details(self):
        body = {"payments": [{"amount": "120.00",
                              "payment_method": self.payment_method()}]}
        response = {"payments": [{"id": self.PAYMENT_ID, "amount": "120.00",
                                  "payment_method": self.payment_method()}]}
        self.respond(lambda: self.order.create_transaction(
            self.ORDER_ID, body, self.options),
            ("POST", "/" + self.ORDER_ID + "/transactions"), response,
            status=201, options=True, body=body)

    def test_update_transaction_forwards_payment_method_and_retains_details(self):
        body = {"payment_method": self.payment_method()}
        response = {"id": self.PAYMENT_ID, "amount": "120.00",
                    "payment_method": self.payment_method()}
        self.respond(lambda: self.order.update_transaction(
            self.ORDER_ID, self.PAYMENT_ID, body, self.options),
            ("PUT", "/" + self.ORDER_ID + "/transactions/" + self.PAYMENT_ID),
            response, options=True, body=body)

    def test_full_and_partial_refund_request_bodies_and_status(self):
        response = {"id": self.ORDER_ID, "status": "processed",
                    "status_detail": "refunded", "transactions": {}}
        partial = {"transactions": [{"id": self.PAYMENT_ID, "amount": "25.00"}]}
        for body, method in (({}, self.order.refund_transaction),
                             (partial, self.order.refund)):
            with self.subTest(body=body):
                self.respond(lambda: method(self.ORDER_ID, body, self.options),
                             ("POST", "/" + self.ORDER_ID + "/refund"),
                             response, status=201, options=True, body=body)

    def test_delete_transaction_returns_no_content(self):
        self.respond(lambda: self.order.delete_transaction(
            self.ORDER_ID, self.PAYMENT_ID),
            ("DELETE", "/" + self.ORDER_ID + "/transactions/" + self.PAYMENT_ID),
            None, status=204)


    def test_manual_creation_without_transactions_then_process(self):
        body = {"type": "online", "processing_mode": "manual",
                "capture_mode": "manual", "total_amount": "100.00",
                "external_reference": "ORDER-2024-001234",
                "payer": {"email": "customer@example.com"}}
        created = {"id": self.ORDER_ID, "status": "created", "type": "online",
                   "processing_mode": "manual", "capture_mode": "manual",
                   "payer": body["payer"]}
        self.respond(lambda: self.order.create(body, self.options),
                     ("POST", ""), created, status=201, options=True, body=body)
        processed = self.order_response()
        self.respond(lambda: self.order.process(self.ORDER_ID, self.options),
                     ("POST", "/" + self.ORDER_ID + "/process"),
                     processed, options=True)

    def test_bank_transfer_request_alternatives_are_serialized_unchanged(self):
        body = {"type": "online", "processing_mode": "automatic",
                "total_amount": "100000.00",
                "payer": {"email": "customer@example.com",
                          "entity_type": "individual",
                          "address": {"city": "Bogota", "state": "DC"}},
                "transactions": {"payments": [{
                    "amount": "100000.00", "expiration_time": "PT20M",
                    "date_of_expiration": "2026-07-01T00:00:00Z",
                    "payment_method": {"id": "pse", "type": "bank_transfer",
                                       "financial_institution": "1051"}}]},
                "config": {"online": {"callback_url": "https://example.com/pse"}},
                "integration_data": {"sponsor_id": 123, "platform_id": "platform-1"}}
        self.respond(lambda: self.order.create(body, self.options),
                     ("POST", ""), self.order_response(), status=201,
                     options=True, body=body)
        payment = body["transactions"]["payments"][0]
        transaction = {"payments": [payment]}
        bank_response = {"payments": [{"id": self.PAYMENT_ID,
                                       "amount": payment["amount"],
                                       "payment_method": {
                                           "id": "pse", "type": "bank_transfer",
                                           "financial_institution": "1051",
                                           "redirect_url": "https://example.com/bank"}}]}
        self.respond(lambda: self.order.create_transaction(
            self.ORDER_ID, transaction, self.options),
            ("POST", "/" + self.ORDER_ID + "/transactions"), bank_response,
            status=201, options=True, body=transaction)
        update = {"payment_method": payment["payment_method"]}
        self.respond(lambda: self.order.update_transaction(
            self.ORDER_ID, self.PAYMENT_ID, update, self.options),
            ("PUT", "/" + self.ORDER_ID + "/transactions/" + self.PAYMENT_ID),
            bank_response["payments"][0], options=True, body=update)

    def test_nested_order_response_fields_survive_all_order_wrappers(self):
        response = self.order_response()
        response["integration_data"] = {"platform_id": "platform-1"}
        response["transactions"]["payments"][0]["payment_method"][
            "transaction_security"] = {
                "status": "pending", "redirect_url": "https://example.com/3ds"}
        operations = (
            (lambda: self.order.create(self.order_body(), self.options), 201),
            (lambda: self.order.get(self.ORDER_ID), 200),
            (lambda: self.order.process(self.ORDER_ID, self.options), 200),
            (lambda: self.order.cancel(self.ORDER_ID, self.options), 200),
            (lambda: self.order.search({"begin_date": "2026-01-01T00:00:00Z",
                                        "end_date": "2026-01-02T00:00:00Z"}), 200),
        )
        for index, (operation, status) in enumerate(operations):
            with self.subTest(operation=index):
                payload = {"data": [response]} if index == 4 else response
                self.http.result = {"status": status, "response": payload}
                result = operation()
                order = result["response"]["data"][0] if index == 4 else result["response"]
                self.assertIs(order, response)
                self.assertEqual(order["payer"]["identification"]["type"], "CPF")
                self.assertEqual(order["items"][0]["category_id"], "electronics")
                self.assertEqual(order["shipment"]["address"]["zip_code"], "01310-100")
                self.assertEqual(order["config"]["online"]["callback_url"],
                                 "https://example.com/callback")
                self.assertEqual(order["integration_data"]["platform_id"], "platform-1")
                self.assertEqual(order["transactions"]["payments"][0][
                    "payment_method"]["token"], "card-token")
                self.assertEqual(order["transactions"]["payments"][0][
                    "payment_method"]["transaction_security"]["status"], "pending")

    def test_transaction_payment_response_fields_survive_sdk_wrapper(self):
        payment = {"id": self.PAYMENT_ID, "amount": "120.00",
                   "payment_method": {"id": "visa", "type": "credit_card",
                                      "token": "card-token", "installments": 2,
                                      "statement_descriptor": "MYSTORE"}}
        add_response = {"payments": [payment]}
        self.http.result = {"status": 201, "response": add_response}
        added = self.order.create_transaction(
            self.ORDER_ID, {"payments": [{"amount": "120.00",
                                         "payment_method": self.payment_method()}]},
            self.options)
        self.assertIs(added["response"]["payments"][0], payment)
        self.assertEqual(added["response"]["payments"][0]["payment_method"][
            "statement_descriptor"], "MYSTORE")
        self.assertEqual(added["response"]["payments"][0]["payment_method"][
            "token"], "card-token")
        self.http.result = {"status": 200, "response": payment}
        updated = self.order.update_transaction(
            self.ORDER_ID, self.PAYMENT_ID,
            {"payment_method": self.payment_method()}, self.options)
        self.assertIs(updated["response"], payment)
        self.assertEqual(updated["response"]["payment_method"]["token"],
                         "card-token")
        self.assertEqual(updated["response"]["payment_method"][
            "installments"], 2)

    def test_refund_full_and_partial_via_refund_method(self):
        full = {}
        partial = {"transactions": [{"id": self.PAYMENT_ID, "amount": "25.00"}]}
        for body in (full, partial):
            with self.subTest(body=body):
                response = {"id": self.ORDER_ID, "status": "processed",
                            "status_detail": "refunded", "transactions": {}}
                self.http.calls.clear()
                self.http.result = {"status": 201, "response": response}
                result = self.order.refund(self.ORDER_ID, body, self.options)
                self.assertEqual(len(self.http.calls), 1)
                verb, call = self.http.calls[0]
                self.assertEqual(verb, "POST")
                self.assertEqual(call["url"], self.BASE + "/" + self.ORDER_ID + "/refund")
                self.assertEqual(call["headers"]["x-idempotency-key"],
                                 self.IDEMPOTENCY_KEY)
                self.assertEqual(json.loads(call["data"]), body)
                self.assertEqual(result["status"], 201)
                self.assertEqual(result["response"]["id"], self.ORDER_ID)
                self.assertEqual(result["response"]["status"], "processed")
                self.assertEqual(result["response"]["status_detail"], "refunded")
                self.assertIs(result["response"]["transactions"], response["transactions"])


if __name__ == "__main__":
    unittest.main()
