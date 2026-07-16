"""Advanced Payment resource for the MercadoPago Marketplace API.

Wraps ``/v1/advanced_payments`` endpoints used in marketplace split-payment
scenarios where funds are distributed among multiple receivers.

`API reference <https://www.mercadopago.com/developers/en/reference>`_
"""
from mercadopago.core import MPBase


class AdvancedPayment(MPBase):
    """Manages split payments in marketplace integrations.

    Advanced payments allow a marketplace to collect a payment and split
    it among multiple sellers in a single transaction.  Use :meth:`search`
    to query advanced payments by filters and :meth:`get` to retrieve
    detailed information about a specific advanced payment.
    """

    def search(self, filters=None, request_options=None):
        """Searches advanced payments matching the given filters.

        Args:
            filters: Query-string parameters (e.g. ``external_reference``,
                ``status``, ``payer_id``).
            request_options: Per-call configuration overrides.

        Returns:
            dict: Paginated list of matching advanced payments.

        Reference: https://www.mercadopago.com/developers/en/reference/advanced_payments/_advanced_payments_search/get
        """
        return self._get(
            uri="/v1/advanced_payments/search",
            filters=filters,
            request_options=request_options,
        )

    def get(self, advanced_payment_id, request_options=None):
        """Retrieves an advanced payment by its ID.

        Args:
            advanced_payment_id: Unique advanced payment identifier.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Full advanced payment object including disbursements,
                payments, and current status.

        Reference: https://www.mercadopago.com/developers/en/reference/advanced_payments/_advanced_payments_id/get
        """
        return self._get(
            uri="/v1/advanced_payments/" + str(advanced_payment_id),
            request_options=request_options,
        )