"""Chargebacks resource for updating chargeback documentation."""
from mercadopago.core import MPBase


class Chargebacks(MPBase):
    """Provides access to chargeback documentation updates."""

    def update_chargeback(self, chargeback_id, chargeback_object, request_options=None):
        """Uploads documentation for an existing chargeback.

        Args:
            chargeback_id: Unique chargeback identifier.
            chargeback_object: JSON body containing the ``files`` array.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Updated chargeback response and HTTP status.
        """
        if not isinstance(chargeback_object, dict):
            raise ValueError("Param chargeback_object must be a Dictionary")

        return self._put(uri="/v1/chargebacks/" + self._path_param(chargeback_id),
                         data=chargeback_object, request_options=request_options)

