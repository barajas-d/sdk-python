"""
    Module: test_preapproval
"""
import os
import unittest
import mercadopago


class TestPreApproval(unittest.TestCase):
    """
    Test Module: PreApproval
    """
    sdk = mercadopago.SDK(os.environ['ACCESS_TOKEN'])

    def test_create(self):
        """
            Function: xoxoxoxo
        """


from tests.base_client_test import BaseClientTest


class TestPreApprovalExport(BaseClientTest):
    """Tests CSV export through the shared binary transport."""

    def test_export_subscriptions(self):
        """Exports subscriptions with query filters and an unmodified CSV body."""
        csv = b"id,status\n1,authorized\n"
        self.mock_http.get_binary.return_value = {"status": 200, "response": csv}

        result = self.sdk.preapproval().export_subscriptions(
            collector_id=42, preapproval_plan_id="plan-1",
            status="authorized", sort="date_created")

        self.mock_http.get_binary.assert_called_once()
        args, kwargs = self.mock_http.get_binary.call_args
        self.assertEqual((), args)
        self.assertEqual("https://api.mercadopago.com/preapproval/export", kwargs["url"])
        self.assertEqual({"collector_id": 42, "preapproval_plan_id": "plan-1",
                          "status": "authorized", "sort": "date_created"}, kwargs["params"])
        self.assertNotIn("data", kwargs)
        self.assertEqual(200, result["status"])
        self.assertEqual(csv, result["response"])

    def test_export_subscriptions_required_collector_only(self):
        """Exports CSV when only the mandatory collector filter is supplied."""
        csv = b"id,status\n2,pending\n"
        self.mock_http.get_binary.return_value = {"status": 200, "response": csv}

        result = self.sdk.preapproval().export_subscriptions(collector_id=42)

        self.mock_http.get_binary.assert_called_once()
        args, kwargs = self.mock_http.get_binary.call_args
        self.assertEqual((), args)
        self.assertEqual("https://api.mercadopago.com/preapproval/export", kwargs["url"])
        self.assertEqual({"collector_id": 42}, kwargs["params"])
        self.assertNotIn("data", kwargs)
        self.assertEqual(200, result["status"])
        self.assertEqual(csv, result["response"])


if __name__ == "__main__":
    unittest.main()
