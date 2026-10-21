"""QR integrator configuration resource for the MercadoPago API."""
from mercadopago.core import MPBase


class QRIntegrator(MPBase):
    """Retrieves the authenticated QR integrator configuration."""

    def create_qr_integrator_config(self, integrator_config_object, request_options=None):
        """Creates or updates the QR integrator configuration.

        Args:
            integrator_config_object: Dict with ``callback_url`` and optional
                ``notification_url``.
            request_options: Per-call configuration overrides.

        Returns:
            dict: HTTP status and integrator configuration response.
        """
        if not isinstance(integrator_config_object, dict):
            raise ValueError("Param integrator_config_object must be a Dictionary")

        return self._patch(uri="/instore/integrator", data=integrator_config_object,
                           request_options=request_options)

    def get_qr_integrator_config(self, request_options=None):
        """Retrieves the QR integrator configuration.

        Args:
            request_options: Per-call configuration overrides.

        Returns:
            dict: HTTP status and integrator configuration response.
        """
        return self._get(uri="/instore/integrator", request_options=request_options)