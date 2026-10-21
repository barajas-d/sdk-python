"""Unit tests for the Claims resource using a mock HTTP client."""
import json
import unittest

from tests.base_client_test import BaseClientTest


class TestClaims(BaseClientTest):
    """Test Module: Claims"""

    def test_get_claim_reasons(self):
        self.mock_get({"id": "reason-1"})

        result = self.sdk.claims().get_claim_reasons("reason-1")

        self.mock_http.get.assert_called_once()
        _, kwargs = self.mock_http.get.call_args
        self.assertEqual(
            "https://api.mercadopago.com/post-purchase/v1/claims/reasons/reason-1",
            kwargs["url"],
        )
        self.assertIsNone(kwargs["params"])
        self.assertNotIn("data", kwargs)
        self.assertEqual(200, result["status"])

    def test_search_claims(self):
        filters = {
            "id": 123,
            "type": "claims",
            "stage": "claim",
            "status": "opened",
            "limit": 10,
            "offset": 5,
        }
        self.mock_get({"results": []})

        result = self.sdk.claims().search_claims(filters=filters)

        self.mock_http.get.assert_called_once()
        _, kwargs = self.mock_http.get.call_args
        self.assertEqual(
            "https://api.mercadopago.com/post-purchase/v1/claims/search",
            kwargs["url"],
        )
        self.assertEqual(filters, kwargs["params"])
        self.assertNotIn("data", kwargs)
        self.assertEqual(200, result["status"])

    def test_get_claim(self):
        self.mock_get({"id": 123})

        result = self.sdk.claims().get_claim(123)

        self.mock_http.get.assert_called_once()
        _, kwargs = self.mock_http.get.call_args
        self.assertEqual(
            "https://api.mercadopago.com/post-purchase/v1/claims/123",
            kwargs["url"],
        )
        self.assertIsNone(kwargs["params"])
        self.assertNotIn("data", kwargs)
        self.assertEqual(200, result["status"])

    def test_attach_claim_file(self):
        file = ("receipt.pdf", b"pdf-content", "application/pdf")
        self.mock_http.request.return_value = {
            "status": 201, "response": {"file_id": "f1", "file_name": "receipt.pdf"}
        }

        result = self.sdk.claims().attach_claim_file(123, file)

        self.mock_http.request.assert_called_once()
        args, kwargs = self.mock_http.request.call_args
        self.assertEqual(("POST",), args)
        self.assertEqual(
            "https://api.mercadopago.com/post-purchase/v1/claims/123/attachments",
            kwargs["url"],
        )
        self.assertEqual({"file": file}, kwargs["files"])
        self.assertIsNone(kwargs["data"])
        self.assertIsNone(kwargs["params"])
        self.assertFalse(any(key.lower() == "content-type" for key in kwargs["headers"]))
        self.assertEqual(201, result["status"])

    def test_get_claim_file(self):
        metadata = {"file_id": "f1", "file_name": "receipt.pdf", "content_type": "application/pdf"}
        self.mock_get(metadata)

        result = self.sdk.claims().get_claim_file(123, "receipt.pdf")

        self.mock_http.get.assert_called_once()
        _, kwargs = self.mock_http.get.call_args
        self.assertEqual(
            "https://api.mercadopago.com/post-purchase/v1/claims/123/attachments/receipt.pdf",
            kwargs["url"],
        )
        self.assertIsNone(kwargs["params"])
        self.assertNotIn("data", kwargs)
        self.assertEqual(200, result["status"])
        self.assertEqual(metadata, result["response"])

    def test_download_claim_file(self):
        content = b"\x00claim-file\xff"
        self.mock_http.get_binary.return_value = {"status": 200, "response": content}

        result = self.sdk.claims().download_claim_file(123, "receipt.pdf")

        self.mock_http.get_binary.assert_called_once()
        args, kwargs = self.mock_http.get_binary.call_args
        self.assertEqual((), args)
        self.assertEqual(
            "https://api.mercadopago.com/post-purchase/v1/claims/123/attachments/receipt.pdf/download",
            kwargs["url"],
        )
        self.assertIsNone(kwargs["params"])
        self.assertNotIn("data", kwargs)
        self.assertEqual(200, result["status"])
        self.assertEqual(content, result["response"])

    def test_get_claim_evidence(self):
        self.mock_get([{"id": "e1"}])

        result = self.sdk.claims().get_claim_evidence(123)

        self.mock_http.get.assert_called_once()
        _, kwargs = self.mock_http.get.call_args
        self.assertEqual(
            "https://api.mercadopago.com/post-purchase/v1/claims/123/evidences",
            kwargs["url"],
        )
        self.assertIsNone(kwargs["params"])
        self.assertNotIn("data", kwargs)
        self.assertEqual(200, result["status"])

    def test_get_claim_mediation_resolutions(self):
        self.mock_get([{"id": "r1"}])

        result = self.sdk.claims().get_claim_mediation_resolutions(123)

        self.mock_http.get.assert_called_once()
        _, kwargs = self.mock_http.get.call_args
        self.assertEqual(
            "https://api.mercadopago.com/post-purchase/v1/claims/123/expected-resolutions",
            kwargs["url"],
        )
        self.assertIsNone(kwargs["params"])
        self.assertNotIn("data", kwargs)
        self.assertEqual(200, result["status"])

    def test_get_claim_messages(self):
        self.mock_get([{"id": "m1"}])

        result = self.sdk.claims().get_claim_messages(123)

        self.mock_http.get.assert_called_once()
        _, kwargs = self.mock_http.get.call_args
        self.assertEqual(
            "https://api.mercadopago.com/post-purchase/v1/claims/123/messages",
            kwargs["url"],
        )
        self.assertIsNone(kwargs["params"])
        self.assertNotIn("data", kwargs)
        self.assertEqual(200, result["status"])

    def test_get_claim_history(self):
        self.mock_get([{"status": "opened"}])

        result = self.sdk.claims().get_claim_history(123)

        self.mock_http.get.assert_called_once()
        _, kwargs = self.mock_http.get.call_args
        self.assertEqual(
            "https://api.mercadopago.com/post-purchase/v1/claims/123/status_history",
            kwargs["url"],
        )
        self.assertIsNone(kwargs["params"])
        self.assertNotIn("data", kwargs)
        self.assertEqual(200, result["status"])

    def test_upload_shipping_evidence(self):
        data = {"type": "tracking_code", "value": "TRACK-123"}
        self.mock_post({"id": "e1"})

        result = self.sdk.claims().upload_shipping_evidence(123, data)

        self.mock_http.post.assert_called_once()
        _, kwargs = self.mock_http.post.call_args
        self.assertEqual(
            "https://api.mercadopago.com/post-purchase/v1/claims/123/actions/evidences",
            kwargs["url"],
        )
        self.assertEqual(data, json.loads(kwargs["data"]))
        self.assertIsNone(kwargs["params"])
        self.assertEqual(201, result["status"])

    def test_request_claim_mediation(self):
        self.mock_post({"id": "123"}, status=200)

        result = self.sdk.claims().request_claim_mediation(123)

        self.mock_http.post.assert_called_once()
        _, kwargs = self.mock_http.post.call_args
        self.assertEqual(
            "https://api.mercadopago.com/post-purchase/v1/claims/123/actions/open-dispute",
            kwargs["url"],
        )
        self.assertIsNone(kwargs["data"])
        self.assertIsNone(kwargs["params"])
        self.assertEqual(200, result["status"])

    def test_send_claim_message(self):
        data = {"message": "Please review", "attachments": ["file-1"]}
        self.mock_post({"id": "m1"})

        result = self.sdk.claims().send_claim_message(123, data, application_id="app-1")

        self.mock_http.post.assert_called_once()
        _, kwargs = self.mock_http.post.call_args
        self.assertEqual(
            "https://api.mercadopago.com/post-purchase/v1/claims/123/actions/send-message",
            kwargs["url"],
        )
        self.assertEqual(data, json.loads(kwargs["data"]))
        self.assertEqual({"application_id": "app-1"}, kwargs["params"])
        self.assertEqual(201, result["status"])


if __name__ == "__main__":
    unittest.main()
