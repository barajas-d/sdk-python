"""Refund resource for the MercadoPago Payments API.

Wraps ``/v1/payments/{payment_id}/refunds`` endpoints to list existing
refunds and create full or partial refunds on approved payments.

Refunds are available within 180 days of payment approval and require
sufficient account balance.

Usage examples::

    import mercadopago
    sdk = mercadopago.SDK("YOUR_ACCESS_TOKEN")

    # Full refund - pass empty dict or None
    result = sdk.refund().create(payment_id, {})
    # or
    result = sdk.refund().create(payment_id)

    # Partial refund - specify amount
    result = sdk.refund().create(payment_id, {'amount': 10.50})

    # With RequestOptions for custom configuration
    from mercadopago.config import RequestOptions
    options = RequestOptions(connection_timeout=30.0)
    result = sdk.refund().create(payment_id, {'amount': 10.50}, request_options=options)

    # List all refunds for a payment
    refunds = sdk.refund().list_all(payment_id)

`API reference <https://www.mercadopago.com/developers/en/reference/online-payments/checkout-api-payments/create-refund/post>`_
"""
from mercadopago.core import MPBase


class Refund(MPBase):
    """Creates and lists refunds for payments.

    Supports full refunds (omit *refund_object* or pass empty dict) and
    partial refunds (pass ``{"amount": <float>}``).  Refunds can only be
    issued for approved payments within 180 days.

    RequestOptions support: All methods accept an optional *request_options*
    parameter to override connection timeout, custom headers, retries, etc.
    """

    def list_all(self, payment_id, request_options=None):
        """Lists all refunds issued for a payment.

        Args:
            payment_id: Identifier of the parent payment.
            request_options: Per-call configuration overrides.

        Returns:
            dict: List of refund objects.

        Reference: https://www.mercadopago.com/developers/en/reference/online-payments/checkout-api-payments/get-refunds/get
        """
        return self._get(uri="/v1/payments/" + str(payment_id) + "/refunds",
                         request_options=request_options)

    def create(self, payment_id, refund_object=None, request_options=None):
        """Creates a refund for a payment.

        Omit *refund_object* or pass an empty dict for a full refund.
        Pass ``{"amount": <float>}`` for a partial refund.

        Examples::

            # Full refund
            sdk.refund().create(payment_id, {})
            # or
            sdk.refund().create(payment_id)

            # Partial refund
            sdk.refund().create(payment_id, {'amount': 10.50})

            # With custom RequestOptions
            from mercadopago.config import RequestOptions
            options = RequestOptions(connection_timeout=30.0)
            sdk.refund().create(payment_id, {'amount': 10.50}, request_options=options)

        Args:
            payment_id: Identifier of the payment to refund.
            refund_object: Optional dict with partial refund details.
                Pass ``{"amount": <float>}`` for partial refund.
                Pass ``{}`` or ``None`` for full refund.
            request_options: Per-call :class:`~mercadopago.config.RequestOptions`
                to override timeout, headers, retries, etc.

        Raises:
            ValueError: If *refund_object* is provided but not a ``dict``.

        Returns:
            dict: Created refund including its ``id`` and ``status``.

        Reference: https://www.mercadopago.com/developers/en/reference/online-payments/checkout-api-payments/create-refund/post
        """
        if refund_object is not None and not isinstance(refund_object, dict):
            raise ValueError("Param refund_object must be a Dictionary")

        return self._post(uri="/v1/payments/" + str(payment_id) + "/refunds",
                          data=refund_object, request_options=request_options)