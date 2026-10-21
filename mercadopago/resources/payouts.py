"""Payouts resource for the MercadoPago Payouts API."""
from mercadopago.core import MPBase


class Payouts(MPBase):
    """Creates payout batches and processes transaction intents."""

    def create_payout(self, payout_object, request_options=None):
        """Creates a batch of payout transactions.

        Args:
            payout_object: Dict containing external_reference and transactions.
            request_options: Per-call configuration overrides.

        Returns:
            dict: API response for the created payout batch.
        """
        if not isinstance(payout_object, dict):
            raise ValueError("Param payout_object must be a Dictionary")

        return self._post(uri="/v1/payouts", data=payout_object,
                          request_options=request_options)

    def process_transaction_intent(self, intent_object, request_options=None):
        """Creates a Pix or bank transfer transaction intent.

        Args:
            intent_object: Dict containing external_reference,
                point_of_interaction and transaction.
            request_options: Per-call configuration overrides.

        Returns:
            dict: API response for the processed transaction intent.
        """
        if not isinstance(intent_object, dict):
            raise ValueError("Param intent_object must be a Dictionary")

        return self._post(uri="/v1/transaction-intents/process", data=intent_object,
                          request_options=request_options)

    def list_payout_transactions(self, payout_id, request_options=None):
        """Lists transactions for a payout batch.

        Args:
            payout_id: Identifier of the payout batch.
            request_options: Per-call configuration overrides.

        Returns:
            dict: API response containing the payout transactions.
        """
        return self._get(uri="/v1/payouts/" + self._path_param(payout_id)
                         + "/transactions", request_options=request_options)

    def get_transaction_intent(self, id, request_options=None):
        """Retrieves a transaction intent by ID.

        Args:
            id: Identifier of the transaction intent.
            request_options: Per-call configuration overrides.

        Returns:
            dict: API response for the transaction intent.
        """
        return self._get(uri="/v1/transaction-intents/" + self._path_param(id),
                         request_options=request_options)

    def cancel_payout_transaction(self, payout_id, transaction_id, request_options=None):
        """Cancels a transaction in a payout batch.

        Args:
            payout_id: Identifier of the payout batch.
            transaction_id: Identifier of the transaction to cancel.
            request_options: Per-call configuration overrides.

        Returns:
            dict: API response for the cancelled transaction.
        """
        return self._put(uri="/v1/payouts/" + self._path_param(payout_id)
                         + "/transactions/" + self._path_param(transaction_id)
                         + "/cancel", request_options=request_options)

    @staticmethod
    def _path_param(value):
        """Encodes an identifier for safe use as a single URL path segment."""
        from urllib.parse import quote
        return quote(str(value), safe="")