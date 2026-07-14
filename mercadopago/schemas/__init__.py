"""Schema classes for the MercadoPago Python SDK.

Provides type definitions and dataclasses for structured request payloads,
particularly for the Orders API.
"""
from mercadopago.schemas.confirm_order_request import ConfirmOrderRequest


__all__ = (
    'ConfirmOrderRequest',
)