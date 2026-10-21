"""Releases report generation and configuration resource."""
from mercadopago.core import MPBase


class ReleasesReport(MPBase):
    """Manage releases reports and their scheduled generation configuration."""

    @staticmethod
    def _path_param(value):
        """Escapes a report identifier as one URL path segment.

        Args:
            value: File name or task identifier to encode.

        Returns:
            str: Percent-encoded path parameter.
        """
        from urllib.parse import quote

        return quote(str(value), safe="")

    def download_release_report(self, file_name, request_options=None):
        """Downloads a generated releases report as raw CSV bytes.

        Args:
            file_name: Name of the generated CSV file.
            request_options: Per-call configuration overrides.

        Returns:
            dict: HTTP status and CSV bytes (or a parsed error response).
        """
        return self._get_binary(
            uri="/v1/account/release_report/" + self._path_param(file_name),
            request_options=request_options,
        )

    def get_release_report(self, request_options=None):
        """Retrieves the list of releases reports.

        Args:
            request_options: Per-call configuration overrides.

        Returns:
            dict: HTTP status and the releases report list.
        """
        return self._get(
            uri="/v1/account/release_report",
            request_options=request_options,
        )

    def create_release_report(self, report_request, request_options=None):
        """Starts generating a releases report for a date range.

        Args:
            report_request: ReportRequest dictionary with ``begin_date`` and
                ``end_date`` in ISO 8601 format.
            request_options: Per-call configuration overrides.

        Returns:
            dict: HTTP status and the report generation task.
        """
        if not isinstance(report_request, dict):
            raise ValueError("Param report_request must be a Dictionary")

        return self._post(
            uri="/v1/account/release_report",
            data=report_request,
            request_options=request_options,
        )

    def get_release_report_config(self, request_options=None):
        """Retrieves the scheduled releases report configuration.

        Args:
            request_options: Per-call configuration overrides.

        Returns:
            dict: HTTP status and the current report configuration.
        """
        return self._get(
            uri="/v1/account/release_report/config",
            request_options=request_options,
        )

    def update_release_report_config(self, report_config, request_options=None):
        """Updates the scheduled releases report configuration.

        Args:
            report_config: ReportConfig dictionary describing the configuration.
            request_options: Per-call configuration overrides.

        Returns:
            dict: HTTP status and the updated report configuration.
        """
        if not isinstance(report_config, dict):
            raise ValueError("Param report_config must be a Dictionary")

        return self._put(
            uri="/v1/account/release_report/config",
            data=report_config,
            request_options=request_options,
        )

    def list_scheduled_release_reports(self, request_options=None):
        """Lists scheduled releases reports.

        Args:
            request_options: Per-call configuration overrides.

        Returns:
            dict: HTTP status and the scheduled report list.
        """
        return self._get(
            uri="/v1/account/release_report/list",
            request_options=request_options,
        )

    def disable_release_report_schedule(self, request_options=None):
        """Disables automatic releases report generation.

        Args:
            request_options: Per-call configuration overrides.

        Returns:
            dict: HTTP status and the schedule disable response.
        """
        return self._delete(
            uri="/v1/account/release_report/schedule",
            request_options=request_options,
        )

    def enable_release_report_schedule(self, request_options=None):
        """Enables automatic releases report generation.

        Args:
            request_options: Per-call configuration overrides.

        Returns:
            dict: HTTP status and the schedule enable response.
        """
        return self._post(
            uri="/v1/account/release_report/schedule",
            request_options=request_options,
        )

    def search_release_reports(self, begin_date, end_date, request_options=None):
        """Searches releases reports for a date range.

        Args:
            begin_date: Start of the search range in ISO 8601 format.
            end_date: End of the search range in ISO 8601 format.
            request_options: Per-call configuration overrides.

        Returns:
            dict: HTTP status and matching reports.
        """
        return self._get(
            uri="/v1/account/release_report/search",
            filters={"begin_date": begin_date, "end_date": end_date},
            request_options=request_options,
        )

    def get_release_report_task(self, task_id, request_options=None):
        """Retrieves the status of a report generation task.

        Args:
            task_id: Identifier of the report generation task.
            request_options: Per-call configuration overrides.

        Returns:
            dict: HTTP status and the report generation task.
        """
        return self._get(
            uri="/v1/account/release_report/task/" + self._path_param(task_id),
            request_options=request_options,
        )

    def create_release_report_config(self, report_config, request_options=None):
        """Creates a scheduled releases report configuration.

        Args:
            report_config: ReportConfig dictionary describing columns,
                schedule, file format, and optional SFTP delivery.
            request_options: Per-call configuration overrides.

        Returns:
            dict: HTTP status and the created report configuration.
        """
        if not isinstance(report_config, dict):
            raise ValueError("Param report_config must be a Dictionary")

        return self._post(
            uri="/v1/account/release_report/config",
            data=report_config,
            request_options=request_options,
        )