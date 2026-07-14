"""ConfirmOrderRequest schema for the MercadoPago Orders API.

Provides a dataclass representing the request body structure for confirming
an order. Use this to build type-safe payloads when calling order confirmation
endpoints.
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class ConfirmOrderRequest:
    """Request body schema for confirming an order.

    Use this dataclass to build the payload when confirming an order through
    the Orders API. Convert to dict with ``dataclasses.asdict()`` before
    passing to the SDK.

    Attributes:
        order_id: Unique identifier of the order to confirm. Type: str.
        confirmation_status: Status to set on the order (e.g. ``"confirmed"``,
            ``"processing"``). Type: str.
        additional_info: Optional metadata or notes related to the confirmation.
            Type: dict.
    """

    order_id: str
    confirmation_status: Optional[str] = None
    additional_info: Optional[dict] = None