"""Claims resource for the MercadoPago post-purchase API."""
from mercadopago.core import MPBase


class Claims(MPBase):
    """Provides read access to post-purchase claims and their metadata."""

    def get_claim_reasons(self, reason_id, request_options=None):
        """Retrieves the description and metadata for a claim reason.

        Args:
            reason_id: Identifier of the claim reason.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Claim reason metadata and HTTP status.
        """
        return self._get(
            uri="/post-purchase/v1/claims/reasons/" + self._path_param(reason_id),
            request_options=request_options,
        )

    def search_claims(self, filters=None, request_options=None):
        """Searches claims using query-string filters.

        Args:
            filters: Query parameters such as id, type, stage, status,
                limit, and offset.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Matching claims and HTTP status.
        """
        if filters is not None and not isinstance(filters, dict):
            raise ValueError("Param filters must be a Dictionary")
        return self._get(
            uri="/post-purchase/v1/claims/search",
            filters=filters,
            request_options=request_options,
        )

    def get_claim(self, claim_id, request_options=None):
        """Retrieves a claim by its identifier.

        Args:
            claim_id: Identifier of the claim.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Claim details and HTTP status.
        """
        return self._get(
            uri="/post-purchase/v1/claims/" + self._path_param(claim_id),
            request_options=request_options,
        )

    def attach_claim_file(self, claim_id, file, request_options=None):
        """Attaches a binary file to a claim using multipart/form-data.

        Args:
            claim_id: Identifier of the claim.
            file: File object or multipart file tuple to attach.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Attached file metadata and HTTP status.
        """
        return self._post_multipart(
            uri="/post-purchase/v1/claims/" + self._path_param(claim_id)
            + "/attachments",
            files={"file": file},
            request_options=request_options,
        )


    def get_claim_file(self, claim_id, file_name, request_options=None):
        """Retrieves JSON metadata for a file attached to a claim.

        Args:
            claim_id: Identifier of the claim.
            file_name: Name of the attached file.
            request_options: Per-call configuration overrides.

        Returns:
            dict: File metadata and HTTP status, not downloaded file content.
        """
        return self._get(
            uri="/post-purchase/v1/claims/" + self._path_param(claim_id)
            + "/attachments/" + self._path_param(file_name),
            request_options=request_options,
        )

    def download_claim_file(self, claim_id, file_name, request_options=None):
        """Downloads the binary content of a file attached to a claim.

        Args:
            claim_id: Identifier of the claim.
            file_name: Name of the attached file.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Downloaded file bytes and HTTP status.
        """
        return self._get_binary(
            uri="/post-purchase/v1/claims/" + self._path_param(claim_id)
            + "/attachments/" + self._path_param(file_name) + "/download",
            filters=None,
            request_options=request_options,
        )

    def get_claim_evidence(self, claim_id, request_options=None):
        """Retrieves evidence associated with a claim.

        Args:
            claim_id: Identifier of the claim.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Claim evidence list and HTTP status.
        """
        return self._get(
            uri="/post-purchase/v1/claims/" + self._path_param(claim_id)
            + "/evidences",
            request_options=request_options,
        )

    def get_claim_mediation_resolutions(self, claim_id, request_options=None):
        """Retrieves expected mediation resolutions for a claim.

        Args:
            claim_id: Identifier of the claim.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Possible resolution options and HTTP status.
        """
        return self._get(
            uri="/post-purchase/v1/claims/" + self._path_param(claim_id)
            + "/expected-resolutions",
            request_options=request_options,
        )

    def get_claim_messages(self, claim_id, request_options=None):
        """Retrieves the messages associated with a claim.

        Args:
            claim_id: Identifier of the claim.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Claim message thread and HTTP status.
        """
        return self._get(
            uri="/post-purchase/v1/claims/" + self._path_param(claim_id)
            + "/messages",
            request_options=request_options,
        )

    def get_claim_history(self, claim_id, request_options=None):
        """Retrieves the status history of a claim.

        Args:
            claim_id: Identifier of the claim.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Claim history entries and HTTP status.
        """
        return self._get(
            uri="/post-purchase/v1/claims/" + self._path_param(claim_id)
            + "/status_history",
            request_options=request_options,
        )

    def upload_shipping_evidence(self, claim_id, data, request_options=None):
        """Uploads JSON shipping evidence for a claim.

        Args:
            claim_id: Identifier of the claim.
            data: Evidence with ``type`` and ``value`` fields.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Upload result and HTTP status.
        """
        if not isinstance(data, dict):
            raise ValueError("Param data must be a Dictionary")
        return self._post(
            uri="/post-purchase/v1/claims/" + self._path_param(claim_id)
            + "/actions/evidences",
            data=data,
            request_options=request_options,
        )

    def request_claim_mediation(self, claim_id, request_options=None):
        """Requests mediation for a claim.

        Args:
            claim_id: Identifier of the claim.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Mediation result and HTTP status.
        """
        return self._post(
            uri="/post-purchase/v1/claims/" + self._path_param(claim_id)
            + "/actions/open-dispute",
            request_options=request_options,
        )

    def send_claim_message(self, claim_id, data, application_id=None, request_options=None):
        """Sends a JSON message in a claim thread.

        Args:
            claim_id: Identifier of the claim.
            data: Message body with ``message`` and optional ``attachments``.
            application_id: Optional application identifier query parameter.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Sent message result and HTTP status.
        """
        if not isinstance(data, dict):
            raise ValueError("Param data must be a Dictionary")
        params = {"application_id": application_id} if application_id is not None else None
        return self._post(
            uri="/post-purchase/v1/claims/" + self._path_param(claim_id)
            + "/actions/send-message",
            data=data,
            params=params,
            request_options=request_options,
        )
