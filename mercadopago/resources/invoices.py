"""Search subscription invoices (authorized payments)."""
from mercadopago.core import MPBase


class Invoices(MPBase):
    """Provides access to subscription billing invoices."""

    def search_authorized_payments(self, filters=None, request_options=None):
        """Searches subscription invoices matching query filters.

        Args:
            filters: Optional query parameters: ``preapproval_id``,
                ``payment_id``, ``payer_id``, ``status``, ``limit``,
                and ``offset``.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Paginated authorized payment search results.
        """
        if filters is not None and not isinstance(filters, dict):
            raise ValueError("Param filters must be a Dictionary")

        return self._get(
            uri="/authorized_payments",
            filters=filters,
            request_options=request_options,
        )