"""
    Module: test_order
"""
import json
import os
import unittest
import random
from datetime import datetime, timezone, timedelta
from time import sleep

import mercadopago
from mercadopago.config import RequestOptions
from mercadopago.http import HttpClient
from tests import api_call_with_retry


class RecordingHttpClient(HttpClient):
    """Records Orders API requests and returns deterministic SDK envelopes."""

    def __init__(self):
        self.calls = []

    def _record(self, method, url, headers, data=None, params=None, **kwargs):
        self.calls.append({
            "method": method,
            "url": url,
            "headers": headers,
            "data": data,
            "params": params,
            **kwargs,
        })
        status = {"POST": 201, "PUT": 200, "DELETE": 204}.get(method, 200)
        if url.endswith(("/cancel", "/process", "/capture")):
            status = 200
        return {"status": status, "response": None if status == 204 else {"id": "ORD123"}}

    def get(self, url, headers, params=None, timeout=None, maxretries=None):
        return self._record("GET", url, headers, params=params,
                            timeout=timeout, maxretries=maxretries)

    def post(self, url, headers, data=None, params=None, timeout=None, maxretries=None):
        return self._record("POST", url, headers, data=data, params=params,
                            timeout=timeout, maxretries=maxretries)

    def put(self, url, headers, data=None, params=None, timeout=None, maxretries=None):
        return self._record("PUT", url, headers, data=data, params=params,
                            timeout=timeout, maxretries=maxretries)

    def delete(self, url, headers, params=None, timeout=None, maxretries=None):
        return self._record("DELETE", url, headers, params=params,
                            timeout=timeout, maxretries=maxretries)


@unittest.skipUnless("ACCESS_TOKEN" in os.environ, "ACCESS_TOKEN is required")
class TestOrder(unittest.TestCase):
    """
    Test Module: Order
    """
    sdk = mercadopago.SDK(os.environ['ACCESS_TOKEN'])

    def create_master_test_card(self, status="APRO"):
        card_token_object = {
            "card_number": "5031433215406351",
            "security_code": "123",
            "expiration_year": "2030",
            "expiration_month": "11",
            "cardholder": {"name": status}
        }
        card_token_created = self.sdk.card_token().create(card_token_object)
        return card_token_created["response"]["id"]

    def create_visa_test_card(self, status="APRO"):
        card_token_object = {
            "card_number": "4235647728025682",
            "security_code": "123",
            "expiration_year": "2030",
            "expiration_month": "11",
            "cardholder": {"name": status}
        }
        card_token_created = self.sdk.card_token().create(card_token_object)
        return card_token_created["response"]["id"]

    def create_order_canceled_or_captured(self, card_token_id):
        random_email_id = random.randint(100000, 999999)
        order_object_cc = {
            "type": "online",
            "processing_mode": "automatic",
            "total_amount": "200.00",
            "external_reference": "ext_ref_1234",
            "payer": {
                "email": f"test_payer_{random_email_id}@testuser.com"
            },
            "capture_mode": "manual",
            "transactions": {
                "payments": [
                    {
                        "amount": "200.00",
                        "payment_method": {
                            "id": "master",
                            "type": "credit_card",
                            "token": card_token_id,
                            "installments": 1
                        }
                    }
                ]
            }
        }
        order_created = self.sdk.order().create(order_object_cc)
        if order_created.get("status") != 201 or not order_created.get("response"):
            self.fail(f"Failed to create order: {order_created}")
        return order_created["response"]["id"]

    def create_order_builder_mode(self):
        random_email_id = random.randint(100000, 999999)
        order_object_cc = {
            "type": "online",
            "processing_mode": "manual",
            "total_amount": "200.00",
            "external_reference": "ext_ref_1234",
            "payer": {
                "email": f"test_payer_{random_email_id}@testuser.com"
            },
        }
        order_created = self.sdk.order().create(order_object_cc)
        if order_created.get("status") != 201 or not order_created.get("response"):
            self.fail(f"Failed to create order: {order_created}")
        return order_created["response"]["id"]

    def create_order_oneshot_mode_complete(self, card_token_id):
        random_email_id = random.randint(100000, 999999)
        order_mode_oneshot_complete = {
            "type": "online",
            "processing_mode": "automatic",
            "total_amount": "200.00",
            "external_reference": "ext_ref_1234",
            "transactions": {
                "payments": [
                    {
                        "amount": "200.00",
                        "payment_method": {
                            "id": "master",
                            "type": "credit_card",
                            "token": card_token_id,
                            "installments": 1
                        }
                    }
                ]
            },
            "payer": {
                "email": f"test_payer_{random_email_id}@testuser.com"
            }
        }

        order_created = self.sdk.order().create(order_mode_oneshot_complete)


        if order_created.get("status") != 201 or not order_created.get("response"):
            self.fail(f"Failed to create order: {order_created}")
        return order_created["response"]

    def create_order_builder_mode_complete(self, card_token_id):
        random_email_id = random.randint(100000, 999999)
        order_mode_builder_complete = {
            "type": "online",
            "processing_mode": "manual",
            "total_amount": "200.00",
            "external_reference": "ext_ref_1234",
            "transactions": {
                "payments": [
                    {
                        "amount": "200.00",
                        "payment_method": {
                            "id": "master",
                            "type": "credit_card",
                            "token": card_token_id,
                            "installments": 12
                        }
                    }
                ]
            },
            "payer": {
                "email": f"test_payer_{random_email_id}@testuser.com"
            }
        }

        order_created = self.sdk.order().create(order_mode_builder_complete)


        if order_created.get("status") != 201 or not order_created.get("response"):
            self.fail(f"Failed to create order: {order_created}")
        return order_created["response"]

    def test_create_order_and_get_by_id(self):
        """
        Test Function: Create an Order and Get an Order by ID
        """
        card_token_id = self.create_master_test_card()
        random_email_id = random.randint(100000, 999999)
        order_object = {
            "type": "online",
            "total_amount": "1000.00",
            "external_reference": "ext_ref_1234",
            "transactions": {
            "payments": [
                {
                "amount": "1000.00",
                "payment_method": {
                    "id": "master",
                    "type": "credit_card",
                    "token": card_token_id,
                    "installments": 12
                }
                }
            ]
            },
            "payer": {
            "email": f"test_payer_{random_email_id}@testuser.com"
            }
        }

        order_created = self.sdk.order().create(order_object)
        self.assertEqual(order_created["status"], 201)
        self.assertEqual(order_created["response"]["status"], "processed")

        order_get =  self.sdk.order().get(order_created["response"]["id"])
        self.assertEqual(order_get["status"], 200)

    def test_process_order(self):
        card_token_id = self.create_master_test_card()
        random_email_id = random.randint(100000, 999999)
        order_object = {
            "type": "online",
            "processing_mode": "manual",
            "external_reference": "ext_ref_1234",
            "total_amount": "200.00",
            "transactions": {
                "payments": [
                    {
                        "amount": "200.00",
                        "payment_method": {
                            "id": "master",
                            "type": "credit_card",
                            "token": card_token_id,
                            "installments": 1
                        }
                    }
                ]
            },
            "payer": {
                "email": f"test_payer_{random_email_id}@testuser.com"
            }
        }

        order_created = self.sdk.order().create(order_object)
        order_id = order_created["response"]["id"]
        process_response = self.sdk.order().process(order_id)
        if process_response.get("status") != 200 or not process_response.get("response"):
            self.fail(f"Failed to create an order: {process_response}")
        self.assertEqual(process_response["status"], 200,
        "Invalid HTTP status when processing the order")

    def test_cancel_order(self):
        card_token_id = self.create_master_test_card()
        order_id = self.create_order_canceled_or_captured(card_token_id)
        order_canceled = api_call_with_retry(
            lambda: self.sdk.order().cancel(order_id), expected_status=200
        )
        self.assertEqual(order_canceled["status"], 200)
        self.assertEqual(order_canceled["response"]["status"], "canceled")

    def test_capture_order(self):
        card_token_id = self.create_master_test_card()
        order_id = self.create_order_canceled_or_captured(card_token_id)
        order_captured = self.sdk.order().capture(order_id)
        self.assertEqual(order_captured["status"], 200)
        self.assertEqual(order_captured["response"]["status"], "processed")

    def test_create_transaction(self):
        card_token_id = self.create_master_test_card()
        order_id = self.create_order_builder_mode()
        transaction_object = {
            "payments": [
                {
                    "amount": "200.00",
                    "payment_method": {
                        "id": "master",
                        "type": "credit_card",
                        "token": card_token_id,
                        "installments": 12
                    }
                }
            ]
        }

        transaction_created = self.sdk.order().create_transaction(order_id, transaction_object)
        self.assertEqual(transaction_created["status"], 201)

    def test_update_transaction(self):
        card_token_id = self.create_master_test_card()
        order_created = self.create_order_builder_mode_complete(card_token_id)
        order_id = order_created["id"]
        transaction_id = order_created["transactions"]["payments"][0]["id"]
        new_card_token_id = self.create_visa_test_card()

        transaction_update = {
            "payment_method": {
                "id": "visa",
                "type": "credit_card",
                "token": new_card_token_id,
                "installments": 5
            }
        }

        transaction_updated = self.sdk.order().update_transaction(order_id, transaction_id,
         transaction_update)
        self.assertEqual(transaction_updated["status"], 200)

    def test_partial_refund_transaction(self):
        card_token_id = self.create_master_test_card()
        order_created = self.create_order_oneshot_mode_complete(card_token_id)
        order_id = order_created["id"]
        transaction_id = order_created["transactions"]["payments"][0]["id"]

        transaction_refund = {
          "transactions": [
            {
              "id": transaction_id,
              "amount": "25.00"
            }
          ]
        }

        transaction_refunded = api_call_with_retry(
            lambda: self.sdk.order().refund_transaction(order_id, transaction_refund),
            expected_status=201
        )
        self.assertIn(transaction_refunded["status"], [201],
                      f"Unexpected status code for refund: {transaction_refunded['status']}."
                      f" Response: {transaction_refunded}")

    def test_refund_transaction(self):
        card_token_id = self.create_master_test_card()
        order_created = self.create_order_oneshot_mode_complete(card_token_id)
        order_id = order_created["id"]
        sleep(3)
        transaction_refunded = api_call_with_retry(
            lambda: self.sdk.order().refund_transaction(order_id), expected_status=201
        )
        self.assertIn(transaction_refunded["status"], [201],
                      f"Unexpected status code for refund: {transaction_refunded['status']}."
                      f" Response: {transaction_refunded}")

    def test_delete_transaction(self):
        card_token_id = self.create_master_test_card()
        order_created = self.create_order_builder_mode_complete(card_token_id)
        order_id = order_created["id"]
        transaction_id = order_created["transactions"]["payments"][0]["id"]
        sleep(3)

        transaction_deleted = self.sdk.order().delete_transaction(order_id, transaction_id)
        self.assertEqual(transaction_deleted["status"], 204)

    def test_search_order(self):
        """
        Test Function: Search Orders
        """
        now = datetime.now(timezone.utc)
        begin_date = (now - timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%SZ")
        end_date = now.strftime("%Y-%m-%dT%H:%M:%SZ")
        search_response = self.sdk.order().search(filters={
            "page": 1,
            "page_size": 10,
            "begin_date": begin_date,
            "end_date": end_date,
        })
        self.assertEqual(search_response["status"], 200)
        self.assertIn("data", search_response["response"])
        self.assertIn("paging", search_response["response"])


class TestOrderContract(unittest.TestCase):
    """Exercises the bounded Orders contract without live credentials."""

    def setUp(self):
        self.http_client = RecordingHttpClient()
        self.sdk = mercadopago.SDK("TEST_ACCESS_TOKEN", http_client=self.http_client)
        self.request_options = RequestOptions(custom_headers={
            "x-idempotency-key": "123e4567-e89b-12d3-a456-426614174000"
        })

    def assert_last_call(self, method, path, status):
        call = self.http_client.calls[-1]
        self.assertEqual(call["method"], method)
        self.assertEqual(call["url"], "https://api.mercadopago.com" + path)
        self.assertEqual(call["headers"]["Authorization"], "Bearer TEST_ACCESS_TOKEN")
        self.assertEqual(status, call["result"]["status"] if "result" in call else status)
        return call

    def test_create_search_and_get_forward_contract_values(self):
        order_object = {
            "type": "online",
            "processing_mode": "automatic",
            "capture_mode": "automatic",
            "total_amount": "100.00",
            "payer": {"email": "buyer@example.com"},
            "transactions": {"payments": [{
                "amount": "100.00",
                "expiration_time": "P1D",
                "payment_method": {
                    "id": "visa",
                    "type": "credit_card",
                    "token": "CARD_TOKEN",
                    "installments": 1,
                },
            }]},
        }
        response = self.sdk.order().create(order_object, self.request_options)
        call = self.http_client.calls[-1]
        self.assertEqual(response["status"], 201)
        self.assertEqual(call["method"], "POST")
        self.assertEqual(call["url"], "https://api.mercadopago.com/v1/orders")
        self.assertEqual(call["headers"]["x-idempotency-key"], "fixed-idempotency-key")
        self.assertEqual(json.loads(call["data"]), order_object)

        filters = {
            "begin_date": "2025-01-01T00:00:00Z",
            "end_date": "2025-01-31T23:59:59Z",
            "external_reference": "ORDER-1",
            "type": "online",
            "status": "processed",
            "limit": 30,
            "offset": 0,
        }
        response = self.sdk.order().search(filters)
        call = self.http_client.calls[-1]
        self.assertEqual(response["status"], 200)
        self.assertEqual(call["method"], "GET")
        self.assertEqual(call["url"], "https://api.mercadopago.com/v1/orders")
        self.assertEqual(call["params"], filters)

        response = self.sdk.order().get("ORD123")
        call = self.http_client.calls[-1]
        self.assertEqual(response["status"], 200)
        self.assertEqual(call["method"], "GET")
        self.assertEqual(call["url"], "https://api.mercadopago.com/v1/orders/ORD123")

    def test_order_actions_forward_idempotency_and_status(self):
        for method_name in ("process", "cancel", "capture"):
            response = getattr(self.sdk.order(), method_name)(
                "ORD123", self.request_options
            )
            call = self.http_client.calls[-1]
            self.assertEqual(response["status"], 200)
            self.assertEqual(call["method"], "POST")
            self.assertEqual(
                call["url"],
                f"https://api.mercadopago.com/v1/orders/ORD123/{method_name}",
            )
            self.assertEqual(
                call["headers"]["x-idempotency-key"], "fixed-idempotency-key"
            )

    def test_transaction_operations_forward_verb_body_and_status(self):
        create_body = {"payments": [{
            "amount": "25.00",
            "payment_method": {"id": "pix", "type": "bank_transfer"},
        }]}
        response = self.sdk.order().create_transaction(
            "ORD123", create_body, self.request_options
        )
        call = self.http_client.calls[-1]
        self.assertEqual(response["status"], 201)
        self.assertEqual(call["method"], "POST")
        self.assertEqual(call["url"],
                         "https://api.mercadopago.com/v1/orders/ORD123/transactions")
        self.assertEqual(json.loads(call["data"]), create_body)
        self.assertEqual(call["headers"]["x-idempotency-key"], "fixed-idempotency-key")

        update_body = {
            "payment_method": {"id": "visa", "type": "credit_card"}
        }
        response = self.sdk.order().update_transaction(
            "ORD123", "TX123", update_body, self.request_options
        )
        call = self.http_client.calls[-1]
        self.assertEqual(response["status"], 200)
        self.assertEqual(call["method"], "PUT")
        self.assertEqual(
            call["url"],
            "https://api.mercadopago.com/v1/orders/ORD123/transactions/TX123",
        )
        self.assertEqual(json.loads(call["data"]), update_body)
        self.assertEqual(call["headers"]["x-idempotency-key"], "fixed-idempotency-key")

        response = self.sdk.order().delete_transaction("ORD123", "TX123")
        call = self.http_client.calls[-1]
        self.assertEqual(response["status"], 204)
        self.assertEqual(call["method"], "DELETE")
        self.assertEqual(
            call["url"],
            "https://api.mercadopago.com/v1/orders/ORD123/transactions/TX123",
        )
        self.assertIsNone(call["data"])

    def test_partial_and_full_refund_body_forwarding(self):
        partial_body = {
            "transactions": [{"id": "TX123", "amount": "10.00"}]
        }
        response = self.sdk.order().refund_transaction(
            "ORD123", partial_body, self.request_options
        )
        call = self.http_client.calls[-1]
        self.assertEqual(response["status"], 201)
        self.assertEqual(call["url"],
                         "https://api.mercadopago.com/v1/orders/ORD123/refund")
        self.assertEqual(json.loads(call["data"]), partial_body)
        self.assertEqual(call["headers"]["x-idempotency-key"], "fixed-idempotency-key")

        response = self.sdk.order().refund_transaction(
            "ORD123", request_options=self.request_options
        )
        call = self.http_client.calls[-1]
        self.assertEqual(response["status"], 201)
        self.assertIsNone(call["data"])
        self.assertEqual(call["headers"]["x-idempotency-key"], "fixed-idempotency-key")


if __name__ == "__main__":
    unittest.main()
