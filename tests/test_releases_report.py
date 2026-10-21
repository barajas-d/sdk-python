"""Unit tests for the ReleasesReport resource using a mock HTTP client."""
import json
import unittest

from tests.base_client_test import BaseClientTest


class TestReleasesReport(BaseClientTest):
    """Test Module: ReleasesReport"""

    def test_download_release_report(self):
        """GET a report CSV without a request body or JSON decoding."""
        csv_bytes = b"release_date,amount\n2026-01-01,42\n"
        self.mock_http.get_binary.return_value = {"status": 200, "response": csv_bytes}

        result = self.sdk.releases_report().download_release_report("report.csv")

        self.mock_http.get_binary.assert_called_once()
        args, kwargs = self.mock_http.get_binary.call_args
        self.assertEqual((), args)
        self.assertEqual(
            "https://api.mercadopago.com/v1/account/release_report/report.csv",
            kwargs["url"],
        )
        self.assertNotIn("data", kwargs)
        self.assertEqual(200, result["status"])
        self.assertEqual(csv_bytes, result["response"])

    def test_get_release_report(self):
        """GET the releases report list without a request body."""
        self.mock_http.get.return_value = {"status": 200, "response": {"results": []}}

        result = self.sdk.releases_report().get_release_report()

        self.mock_http.get.assert_called_once()
        args, kwargs = self.mock_http.get.call_args
        self.assertEqual((), args)
        self.assertEqual("https://api.mercadopago.com/v1/account/release_report", kwargs["url"])
        self.assertNotIn("data", kwargs)
        self.assertEqual(200, result["status"])

    def test_create_release_report(self):
        """POST a ReportRequest as JSON to generate a report."""
        payload = {"begin_date": "2026-01-01", "end_date": "2026-01-31"}
        self.mock_http.post.return_value = {"status": 202, "response": {"id": "1"}}

        result = self.sdk.releases_report().create_release_report(payload)

        self.mock_http.post.assert_called_once()
        args, kwargs = self.mock_http.post.call_args
        self.assertEqual((), args)
        self.assertEqual("https://api.mercadopago.com/v1/account/release_report", kwargs["url"])
        self.assertEqual(payload, json.loads(kwargs["data"]))
        self.assertEqual(202, result["status"])

    def test_get_release_report_config(self):
        """GET the current releases report configuration."""
        self.mock_http.get.return_value = {"status": 200, "response": {"columns": []}}

        result = self.sdk.releases_report().get_release_report_config()

        self.mock_http.get.assert_called_once()
        args, kwargs = self.mock_http.get.call_args
        self.assertEqual((), args)
        self.assertEqual("https://api.mercadopago.com/v1/account/release_report/config", kwargs["url"])
        self.assertNotIn("data", kwargs)
        self.assertEqual(200, result["status"])

    def test_create_release_report_config(self):
        """POST a ReportConfig as JSON."""
        payload = {"columns": ["release_date"], "frequency": "daily", "file_format": "csv"}
        self.mock_http.post.return_value = {"status": 200, "response": payload}

        result = self.sdk.releases_report().create_release_report_config(payload)

        self.mock_http.post.assert_called_once()
        args, kwargs = self.mock_http.post.call_args
        self.assertEqual((), args)
        self.assertEqual("https://api.mercadopago.com/v1/account/release_report/config", kwargs["url"])
        self.assertEqual(payload, json.loads(kwargs["data"]))
        self.assertEqual(200, result["status"])

    def test_update_release_report_config(self):
        """PUT the updated ReportConfig as JSON."""
        payload = {"columns": ["release_date"], "frequency": "daily", "file_format": "csv"}
        self.mock_http.put.return_value = {"status": 200, "response": payload}

        result = self.sdk.releases_report().update_release_report_config(payload)

        self.mock_http.put.assert_called_once()
        args, kwargs = self.mock_http.put.call_args
        self.assertEqual((), args)
        self.assertEqual("https://api.mercadopago.com/v1/account/release_report/config", kwargs["url"])
        self.assertEqual(payload, json.loads(kwargs["data"]))
        self.assertEqual(200, result["status"])

    def test_list_scheduled_release_reports(self):
        """GET the scheduled releases reports without a body."""
        self.mock_http.get.return_value = {"status": 200, "response": {"results": []}}

        result = self.sdk.releases_report().list_scheduled_release_reports()

        self.mock_http.get.assert_called_once()
        args, kwargs = self.mock_http.get.call_args
        self.assertEqual((), args)
        self.assertEqual("https://api.mercadopago.com/v1/account/release_report/list", kwargs["url"])
        self.assertNotIn("data", kwargs)
        self.assertEqual(200, result["status"])

    def test_disable_release_report_schedule(self):
        """DELETE scheduled generation without a body."""
        self.mock_http.delete.return_value = {"status": 200, "response": None}

        result = self.sdk.releases_report().disable_release_report_schedule()

        self.mock_http.delete.assert_called_once()
        args, kwargs = self.mock_http.delete.call_args
        self.assertEqual((), args)
        self.assertEqual("https://api.mercadopago.com/v1/account/release_report/schedule", kwargs["url"])
        self.assertNotIn("data", kwargs)
        self.assertEqual(200, result["status"])

    def test_enable_release_report_schedule(self):
        """POST scheduled generation without a JSON body."""
        self.mock_http.post.return_value = {"status": 200, "response": None}

        result = self.sdk.releases_report().enable_release_report_schedule()

        self.mock_http.post.assert_called_once()
        args, kwargs = self.mock_http.post.call_args
        self.assertEqual((), args)
        self.assertEqual("https://api.mercadopago.com/v1/account/release_report/schedule", kwargs["url"])
        self.assertIsNone(kwargs["data"])
        self.assertEqual(200, result["status"])


if __name__ == "__main__":
    unittest.main()