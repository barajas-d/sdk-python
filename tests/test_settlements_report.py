"""Unit tests for the SettlementsReport resource using a mock HTTP client."""
import json
import unittest

from mercadopago.resources import SettlementsReport
from tests.base_client_test import BaseClientTest


class TestSettlementsReport(BaseClientTest):
    """Test Module: SettlementsReport."""

    def test_get_settlement_report(self):
        """Lists settlement reports without sending a request body."""
        self.mock_http.get.return_value = {"status": 200, "response": {"results": []}}

        resource = self.sdk.settlements_report()
        self.assertIsInstance(resource, SettlementsReport)
        result = resource.get_settlement_report()

        self.mock_http.get.assert_called_once()
        _, kwargs = self.mock_http.get.call_args
        self.assertEqual("https://api.mercadopago.com/v1/account/settlement_report",
                         kwargs["url"])
        self.assertNotIn("data", kwargs)
        self.assertEqual(200, result["status"])

    def test_create_settlement_report(self):
        """Creates a report with the ReportRequest JSON body."""
        payload = {"begin_date": "2025-01-01", "end_date": "2025-01-31"}
        self.mock_http.post.return_value = {"status": 202, "response": {"id": "1"}}

        result = self.sdk.settlements_report().create_settlement_report(payload)

        self.mock_http.post.assert_called_once()
        _, kwargs = self.mock_http.post.call_args
        self.assertEqual("https://api.mercadopago.com/v1/account/settlement_report",
                         kwargs["url"])
        self.assertEqual(payload, json.loads(kwargs["data"]))
        self.assertEqual(202, result["status"])

    def test_get_settlement_report_config(self):
        """Gets the configuration without sending a request body."""
        self.mock_http.get.return_value = {"status": 200, "response": {}}

        result = self.sdk.settlements_report().get_settlement_report_config()

        self.mock_http.get.assert_called_once()
        _, kwargs = self.mock_http.get.call_args
        self.assertEqual("https://api.mercadopago.com/v1/account/settlement_report/config",
                         kwargs["url"])
        self.assertNotIn("data", kwargs)
        self.assertEqual(200, result["status"])

    def test_create_settlement_report_config(self):
        """Creates the configuration with a ReportConfig JSON body."""
        payload = {"columns": ["DATE", "TRANSACTION_ID"], "frequency": "daily"}
        self.mock_http.post.return_value = {"status": 200, "response": payload}

        result = self.sdk.settlements_report().create_settlement_report_config(payload)

        self.mock_http.post.assert_called_once()
        _, kwargs = self.mock_http.post.call_args
        self.assertEqual("https://api.mercadopago.com/v1/account/settlement_report/config",
                         kwargs["url"])
        self.assertEqual(payload, json.loads(kwargs["data"]))
        self.assertEqual(200, result["status"])

    def test_update_settlement_report_config(self):
        """Updates configuration with a JSON PUT body."""
        payload = {"columns": ["DATE"], "frequency": "daily"}
        self.mock_http.put.return_value = {"status": 200, "response": payload}

        result = self.sdk.settlements_report().update_settlement_report_config(payload)

        self.mock_http.put.assert_called_once()
        _, kwargs = self.mock_http.put.call_args
        self.assertEqual("https://api.mercadopago.com/v1/account/settlement_report/config",
                         kwargs["url"])
        self.assertEqual(payload, json.loads(kwargs["data"]))
        self.assertEqual(200, result["status"])

    def test_list_scheduled_settlement_reports(self):
        """Lists scheduled reports without a body."""
        self.mock_http.get.return_value = {"status": 200, "response": {"results": []}}

        result = self.sdk.settlements_report().list_scheduled_settlement_reports()

        self.mock_http.get.assert_called_once()
        _, kwargs = self.mock_http.get.call_args
        self.assertEqual("https://api.mercadopago.com/v1/account/settlement_report/list",
                         kwargs["url"])
        self.assertNotIn("data", kwargs)
        self.assertEqual(200, result["status"])

    def test_disable_settlement_report_schedule(self):
        """Disables scheduling without a body."""
        self.mock_http.delete.return_value = {"status": 200, "response": None}

        result = self.sdk.settlements_report().disable_settlement_report_schedule()

        self.mock_http.delete.assert_called_once()
        _, kwargs = self.mock_http.delete.call_args
        self.assertEqual("https://api.mercadopago.com/v1/account/settlement_report/schedule",
                         kwargs["url"])
        self.assertNotIn("data", kwargs)
        self.assertEqual(200, result["status"])

    def test_enable_settlement_report_schedule(self):
        """Enables scheduling without a required body."""
        self.mock_http.post.return_value = {"status": 200, "response": None}

        result = self.sdk.settlements_report().enable_settlement_report_schedule()

        self.mock_http.post.assert_called_once()
        _, kwargs = self.mock_http.post.call_args
        self.assertEqual("https://api.mercadopago.com/v1/account/settlement_report/schedule",
                         kwargs["url"])
        self.assertIsNone(kwargs["data"])
        self.assertEqual(200, result["status"])

    def test_search_settlement_reports(self):
        """Passes the report date range as query parameters."""
        self.mock_http.get.return_value = {"status": 200, "response": {"results": []}}

        result = self.sdk.settlements_report().search_settlement_reports(
            begin_date="2025-01-01T00:00:00Z", end_date="2025-01-31T23:59:59Z")

        self.mock_http.get.assert_called_once()
        _, kwargs = self.mock_http.get.call_args
        self.assertEqual("https://api.mercadopago.com/v1/account/settlement_report/search",
                         kwargs["url"])
        self.assertEqual({"begin_date": "2025-01-01T00:00:00Z",
                          "end_date": "2025-01-31T23:59:59Z"}, kwargs["params"])
        self.assertEqual(200, result["status"])

    def test_download_settlement_report(self):
        """Downloads raw CSV bytes without a request body."""
        csv = b"date,amount\n2025-01-01,10\n"
        self.mock_http.get_binary.return_value = {"status": 200, "response": csv}

        result = self.sdk.settlements_report().download_settlement_report("report.csv")

        self.mock_http.get_binary.assert_called_once()
        _, kwargs = self.mock_http.get_binary.call_args
        self.assertEqual("https://api.mercadopago.com/v1/account/settlement_report/report.csv",
                         kwargs["url"])
        self.assertNotIn("data", kwargs)
        self.assertEqual(200, result["status"])
        self.assertEqual(csv, result["response"])

    def test_download_settlement_report_encodes_path(self):
        """Escapes file names as one path segment and preserves raw CSV bytes."""
        csv = b"date,amount\n2025-01-01,10\n"
        self.mock_http.get_binary.return_value = {"status": 200, "response": csv}

        result = self.sdk.settlements_report().download_settlement_report("a/b.csv")

        self.mock_http.get_binary.assert_called_once()
        _, kwargs = self.mock_http.get_binary.call_args
        self.assertEqual("https://api.mercadopago.com/v1/account/settlement_report/a%2Fb.csv",
                         kwargs["url"])
        self.assertNotIn("data", kwargs)
        self.assertEqual(200, result["status"])
        self.assertEqual(csv, result["response"])

    def test_get_settlement_report_task(self):
        """Gets the requested task without sending a request body."""
        self.mock_http.get.return_value = {"status": 200, "response": {"id": "task-1"}}

        result = self.sdk.settlements_report().get_settlement_report_task("task-1")

        self.mock_http.get.assert_called_once()
        _, kwargs = self.mock_http.get.call_args
        self.assertEqual("https://api.mercadopago.com/v1/account/settlement_report/task/task-1",
                         kwargs["url"])
        self.assertNotIn("data", kwargs)
        self.assertEqual(200, result["status"])

    def test_get_settlement_report_task_encodes_path(self):
        """Escapes task IDs as a single path segment on GET."""
        self.mock_http.get.return_value = {"status": 200, "response": {"id": "a/b"}}

        result = self.sdk.settlements_report().get_settlement_report_task("a/b")

        self.mock_http.get.assert_called_once()
        _, kwargs = self.mock_http.get.call_args
        self.assertEqual("https://api.mercadopago.com/v1/account/settlement_report/task/a%2Fb",
                         kwargs["url"])
        self.assertNotIn("data", kwargs)
        self.assertEqual(200, result["status"])


if __name__ == "__main__":
    unittest.main()