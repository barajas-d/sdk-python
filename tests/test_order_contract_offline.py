"""Credential-free wire contract tests for Order refund requests."""
import unittest
from unittest.mock import Mock

from mercadopago.config.request_options import RequestOptions
from mercadopago.resources.order import Order


class TestOrderRefundOffline(unittest.TestCase):
    """Exercise the public refund method through MPBase's JSON transport."""

    def setUp(self):
        self.http = Mock()
        self.response = {"status": 201, "response": {"id": "ORD-123", "status": "refunded"}}
        self.http.post.return_value = self.response
        self.order = Order(RequestOptions(access_token="offline-token"), self.http)
        self.url = "https://api.mercadopago.com/v1/orders/ORD-123/refund"

    def assert_refund_wire(self, expected_data, options=None):
        """Check the exact JSON string and the route sent to the fake client."""
        call = self.http.post.call_args
        self.assertEqual(call.kwargs["url"], self.url)
        self.assertEqual(call.kwargs["data"], expected_data)
        self.assertIsNone(call.kwargs["params"])
        self.assertEqual(call.kwargs["headers"]["Content-type"], "application/json")
        self.assertEqual(call.kwargs["headers"]["Authorization"], "Bearer offline-token")
        if options is not None:
            self.assertEqual(call.kwargs["headers"]["x-test-refund"], "override")
            self.assertEqual(call.kwargs["timeout"], options.connection_timeout)
            self.assertEqual(call.kwargs["maxretries"], options.max_retries)
        self.http.post.assert_called_once()

    def test_partial_transaction_refund_serializes_nested_id_and_amount(self):
        payload = {"transactions": [{"id": "PAY-456", "amount": "25.00"}]}
        options = RequestOptions(
            access_token="offline-token", custom_headers={"x-test-refund": "override"},
            connection_timeout=12.0, max_retries=1,
        )
        result = self.order.refund_transaction("ORD-123", payload, request_options=options)
        self.assertIs(result, self.response)
        self.assert_refund_wire(
            '{"transactions": [{"id": "PAY-456", "amount": "25.00"}]}', options,
        )
        self.assertEqual(payload, {"transactions": [{"id": "PAY-456", "amount": "25.00"}]})

    def test_checkout_pro_split_refund_uses_user_id(self):
        payload = {"splits": [{"user_id": 123, "amount": "50.00"}, {"user_id": 456}]}
        result = self.order.refund_transaction("ORD-123", payload)
        self.assertIs(result, self.response)
        self.assert_refund_wire(
            '{"splits": [{"user_id": 123, "amount": "50.00"}, {"user_id": 456}]}'
        )

    def test_split_one_to_many_refund_uses_receiver_id(self):
        payload = {"splits": [
            {"receiver_id": "receiver-1", "amount": "25.00"},
            {"receiver_id": "receiver-2"},
        ]}
        result = self.order.refund_transaction("ORD-123", payload)
        self.assertIs(result, self.response)
        self.assert_refund_wire(
            '{"splits": [{"receiver_id": "receiver-1", "amount": "25.00"}, '
            '{"receiver_id": "receiver-2"}]}'
        )

    def test_full_refund_sends_no_body_and_preserves_response(self):
        response = {"status": 201, "response": {"id": "ORD-123", "status": "refunded"}}
        self.http.post.return_value = response
        self.assertIs(self.order.refund_transaction("ORD-123"), response)
        self.assert_refund_wire(None)

    def test_explicit_none_stays_bodyless(self):
        self.assertIs(self.order.refund_transaction("ORD-123", None), self.response)
        self.assert_refund_wire(None)

    def test_nested_transactions_are_forwarded_without_flattening(self):
        payload = {"transactions": [
            {"id": "PAY-456", "amount": "25.00"},
            {"id": "PAY-789"},
        ]}
        self.assertIs(self.order.refund_transaction("ORD-123", payload), self.response)
        self.assert_refund_wire(
            '{"transactions": [{"id": "PAY-456", "amount": "25.00"}, '
            '{"id": "PAY-789"}]}'
        )

    def test_bodyless_refund_preserves_no_content_response(self):
        no_content = {"status": 204, "response": None}
        self.http.post.return_value = no_content
        self.assertIs(self.order.refund_transaction("ORD-123"), no_content)
        self.assert_refund_wire(None)


class TestOrderPointEventOffline(unittest.TestCase):
    """Exercise Point test-order events through the existing JSON transport."""

    def setUp(self):
        self.http = Mock()
        self.no_content = {"status": 204, "response": None}
        self.http.post.return_value = self.no_content
        self.order = Order(RequestOptions(access_token="offline-token"), self.http)

    def test_create_event_serializes_status_and_optional_fields_with_custom_headers(self):
        event = {
            "status": "processed", "status_detail": "accredited",
            "payment_method_type": "credit_card", "installments": 2,
            "payment_method_id": "visa",
        }
        options = RequestOptions(
            access_token="offline-token", custom_headers={"x-test-event": "enabled"},
            connection_timeout=12.0, max_retries=1,
        )

        result = self.order.create_event("ORD-123", event, request_options=options)

        self.assertIs(result, self.no_content)
        self.http.post.assert_called_once()
        wire = self.http.post.call_args.kwargs
        self.assertEqual(wire["url"], "https://api.mercadopago.com/v1/orders/ORD-123/events")
        self.assertEqual(
            wire["data"],
            '{"status": "processed", "status_detail": "accredited", '
            '"payment_method_type": "credit_card", "installments": 2, '
            '"payment_method_id": "visa"}',
        )
        self.assertIsNone(wire["params"])
        self.assertEqual(wire["headers"]["Authorization"], "Bearer offline-token")
        self.assertEqual(wire["headers"]["Content-type"], "application/json")
        self.assertEqual(wire["headers"]["x-test-event"], "enabled")
        self.assertEqual(wire["timeout"], 12.0)
        self.assertEqual(wire["maxretries"], 1)
        self.assertEqual(event["status"], "processed")

    def test_create_event_with_only_required_status_preserves_no_content(self):
        result = self.order.create_event("ORD-123", {"status": "canceled"})

        self.assertIs(result, self.no_content)
        self.http.post.assert_called_once()
        wire = self.http.post.call_args.kwargs
        self.assertEqual(wire["url"], "https://api.mercadopago.com/v1/orders/ORD-123/events")
        self.assertEqual(wire["data"], '{"status": "canceled"}')
        self.assertIsNone(wire["params"])
        self.assertEqual(wire["headers"]["Content-type"], "application/json")


if __name__ == "__main__":
    unittest.main()
