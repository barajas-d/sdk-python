"""Refund resource for the MercadoPago Payments API.

Wraps ``/v1/payments/{payment_id}/refunds`` endpoints to list existing
refunds and create full or partial refunds on approved payments.

Refunds are available within 180 days of payment approval and require
sufficient account balance.

`API reference <https://www.mercadopago.com/developers/en/reference/online-payments/checkout-api-payments/create-refund/post>`_
"""
from dataclasses import dataclass
from typing import List, Optional
from mercadopago.core import MPBase


@dataclass
class RefundsResponse:
    """Schema for the response structure from the refund endpoint.

    Represents the structured response returned when creating or listing
    refunds for a payment. This schema helps developers understand and
    work with the refund API response data.

    Attributes:
        id: Unique identifier for the refund. Type: int or str.
        payment_id: Identifier of the parent payment being refunded. Type: int or str.
        amount: Refund amount. Type: float.
        status: Current status of the refund (e.g., ``"approved"``, ``"pending"``,
            ``"rejected"``). Type: str.
        date_created: ISO 8601 timestamp when the refund was created. Type: str.
        metadata: Optional metadata associated with the refund. Type: dict.
        source: Optional information about the refund source. Type: dict.
        unique_sequence_number: Optional unique sequence number for tracking. Type: str.
        refund_mode: Optional mode of the refund (e.g., ``"standard"``). Type: str.
        adjustment_amount: Optional adjustment amount applied. Type: float.
        reason: Optional reason for the refund. Type: str.
    """

    id: Optional[int] = None
    payment_id: Optional[int] = None
    amount: Optional[float] = None
    status: Optional[str] = None
    date_created: Optional[str] = None
    metadata: Optional[dict] = None
    source: Optional[dict] = None
    unique_sequence_number: Optional[str] = None
    refund_mode: Optional[str] = None
    adjustment_amount: Optional[float] = None
    reason: Optional[str] = None


class Refund(MPBase):
    """Creates and lists refunds for payments.

    Supports full refunds (omit *refund_object*) and partial refunds
    (pass ``{"amount": <float>}``).  Refunds can only be issued for
    approved payments within 180 days.
    """

    def list_all(self, payment_id, request_options=None):
        """Lists all refunds issued for a payment.

        Args:
            payment_id: Identifier of the parent payment.
            request_options: Per-call configuration overrides.

        Returns:
            dict: List of refund objects. The response data can be mapped
                to :class:`RefundsResponse` instances for structured access.

        Reference: https://www.mercadopago.com/developers/en/reference/online-payments/checkout-api-payments/get-refunds/get
        """
        return self._get(uri="/v1/payments/" + str(payment_id) + "/refunds",
                         request_options=request_options)

    def create(self, payment_id, refund_object=None, request_options=None):
        """Creates a refund for a payment.

        Omit *refund_object* for a full refund, or pass
        ``{"amount": <float>}`` for a partial refund.

        Args:
            payment_id: Identifier of the payment to refund.
            refund_object: Optional dict with partial refund details.
            request_options: Per-call configuration overrides.

        Raises:
            ValueError: If *refund_object* is provided but not a ``dict``.

        Returns:
            dict: Created refund including its ``id`` and ``status``. The
                response data can be mapped to a :class:`RefundsResponse`
                instance for structured access.

        Reference: https://www.mercadopago.com/developers/en/reference/online-payments/checkout-api-payments/create-refund/post
        """
        if refund_object is not None and not isinstance(refund_object, dict):
            raise ValueError("Param refund_object must be a Dictionary")

        return self._post(uri="/v1/payments/" + str(payment_id) + "/refunds",
                          data=refund_object, request_options=request_options)