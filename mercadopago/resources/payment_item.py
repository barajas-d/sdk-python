"""PaymentItem data model for the MercadoPago API.

Represents an item in a payment request with details such as title,
description, quantity, and unit price.
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class PaymentItem:
    """Data model for a payment item.

    Use this dataclass to build item payloads for payment requests.
    Convert to dict with ``dataclasses.asdict()``.

    Attributes:
        id: Optional item identifier. Type: str.
        title: Optional item title or name. Type: str.
        description: Optional item description. Type: str.
        category_id: Optional category identifier for the item. Type: str.
        quantity: Optional number of items. Type: int.
        unit_price: Optional price per unit. Type: float.
    """

    id: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    category_id: Optional[str] = None
    quantity: Optional[int] = None
    unit_price: Optional[float] = None