"""QR orders resource for cash withdrawal confirmations."""
from urllib.parse import quote

from mercadopago.core import MPBase


class QROrders(MPBase):
    """Manages QR-based cash withdrawal orders."""

    @staticmethod
    def _path_param(value):
        """Escapes a path parameter without allowing it to alter the URI."""
        return quote(str(value), safe="")

    def confirm_cashout_qr(self, merchant_order_id, confirmation_object, request_options=None):
        """Confirms or cancels a QR cashout order.

        Args:
            merchant_order_id: Identifier of the merchant order to confirm.
            confirmation_object: Dict containing ``status`` (``confirmed`` or
                ``cancelled``).
            request_options: Per-call configuration overrides.

        Returns:
            dict: Cashout confirmation response and HTTP status.
        """
        if not isinstance(confirmation_object, dict):
            raise ValueError("Param confirmation_object must be a Dictionary")

        return self._post(
            uri=f"/instore/orders/{self._path_param(merchant_order_id)}/confirmation",
            data=confirmation_object,
            request_options=request_options,
        )