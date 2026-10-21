"""Settlements report resource for the MercadoPago API.

Supports on-demand report generation and scheduled report configuration.
"""
from mercadopago.core import MPBase


class SettlementsReport(MPBase):
    def download_settlement_report(self, file_name, request_options=None):
        """Downloads a settlement report as raw CSV bytes.

        Args:
            file_name: Name of the settlement report file to download.
            request_options: Per-call configuration overrides.

        Returns:
            dict: HTTP status and unparsed CSV response bytes.
        """
        return self._get_binary(
            uri="/v1/account/settlement_report/" + self._path_param(file_name),
            request_options=request_options,
        )

    def update_settlement_report_config(self, report_config, request_options=None):
        """Updates scheduled settlement report configuration.

        Args:
            report_config: ReportConfig dict with scheduling settings.
            request_options: Per-call configuration overrides.

        Returns:
            dict: HTTP status and the updated report configuration.
        """
        if not isinstance(report_config, dict):
            raise ValueError("Param report_config must be a Dictionary")
        return self._put(
            uri="/v1/account/settlement_report/config",
            data=report_config,
            request_options=request_options,
        )

    def list_scheduled_settlement_reports(self, request_options=None):
        """Lists scheduled settlement reports.

        Args:
            request_options: Per-call configuration overrides.

        Returns:
            dict: HTTP status and the scheduled report list.
        """
        return self._get(
            uri="/v1/account/settlement_report/list",
            request_options=request_options,
        )

    def disable_settlement_report_schedule(self, request_options=None):
        """Disables automatic settlement report generation.

        Args:
            request_options: Per-call configuration overrides.

        Returns:
            dict: HTTP status and the disable response.
        """
        return self._delete(
            uri="/v1/account/settlement_report/schedule",
            request_options=request_options,
        )

    def enable_settlement_report_schedule(self, request_options=None):
        """Enables automatic settlement report generation.

        Args:
            request_options: Per-call configuration overrides.

        Returns:
            dict: HTTP status and the enable response.
        """
        return self._post(
            uri="/v1/account/settlement_report/schedule",
            request_options=request_options,
        )
    """Manages settlement reports and their automatic generation settings."""

    def get_settlement_report(self, request_options=None):
        """Retrieves the list of settlement reports.

        Args:
            request_options: Per-call configuration overrides.

        Returns:
            dict: HTTP status and the report list response.
        """
        return self._get(
            uri="/v1/account/settlement_report",
            request_options=request_options,
        )

    def create_settlement_report(self, report_request, request_options=None):
        """Starts generation of a report for a specified date range.

        Args:
            report_request: ReportRequest dict with ``begin_date`` and ``end_date``.
            request_options: Per-call configuration overrides.

        Returns:
            dict: HTTP status and the report-generation task.
        """
        if not isinstance(report_request, dict):
            raise ValueError("Param report_request must be a Dictionary")

        return self._post(
            uri="/v1/account/settlement_report",
            data=report_request,
            request_options=request_options,
        )

    def get_settlement_report_config(self, request_options=None):
        """Retrieves the current settlement report configuration.

        Args:
            request_options: Per-call configuration overrides.

        Returns:
            dict: HTTP status and the current report configuration.
        """
        return self._get(
            uri="/v1/account/settlement_report/config",
            request_options=request_options,
        )

    def search_settlement_reports(self, begin_date=None, end_date=None,
                                  request_options=None):
        """Searches settlement reports within a date range.

        Args:
            begin_date: Optional starting date-time of the search.
            end_date: Optional ending date-time of the search.
            request_options: Per-call configuration overrides.

        Returns:
            dict: HTTP status and matching settlement reports.
        """
        filters = {}
        if begin_date is not None:
            filters["begin_date"] = begin_date
        if end_date is not None:
            filters["end_date"] = end_date
        return self._get(
            uri="/v1/account/settlement_report/search",
            filters=filters,
            request_options=request_options,
        )

    def get_settlement_report_task(self, task_id, request_options=None):
        """Retrieves the status of a settlement report generation task.

        Args:
            task_id: Identifier of the report generation task.
            request_options: Per-call configuration overrides.

        Returns:
            dict: HTTP status and report task details.
        """
        return self._get(
            uri="/v1/account/settlement_report/task/" + self._path_param(task_id),
            request_options=request_options,
        )

    def create_settlement_report_config(self, report_config, request_options=None):
        """Creates the configuration for scheduled settlement reports.

        Args:
            report_config: ReportConfig dict with columns and scheduling settings.
            request_options: Per-call configuration overrides.

        Returns:
            dict: HTTP status and the created report configuration.
        """
        if not isinstance(report_config, dict):
            raise ValueError("Param report_config must be a Dictionary")

        return self._post(
            uri="/v1/account/settlement_report/config",
            data=report_config,
            request_options=request_options,
        )