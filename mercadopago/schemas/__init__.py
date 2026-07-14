"""Schema definitions for MercadoPago API responses.

Provides type definitions and data classes for structured responses
returned by the MercadoPago API, enabling better IDE support and
type checking for response objects.
"""
from mercadopago.schemas.order_op_response import OrderOPResponse


__all__ = (
    'OrderOPResponse',
)