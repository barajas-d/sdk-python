"""PaymentAdditionalInfo data model for fraud scoring.

Defines the structure for additional information attached to payment requests
to improve fraud detection and risk assessment. This data is used by
MercadoPago's fraud-scoring engine.

`API reference
<https://www.mercadopago.com/developers/en/reference/online-payments/checkout-api-payments/create-payment/post>`_
"""
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class PaymentItem:
    """Item purchased in the payment.

    Attributes:
        id: Item identifier. Type: str.
        title: Item title or name. Type: str.
        description: Item description. Type: str.
        picture_url: URL of the item picture. Type: str.
        category_id: Category identifier. Type: str.
        quantity: Quantity purchased. Type: int.
        unit_price: Price per unit. Type: float.
    """

    id: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    picture_url: Optional[str] = None
    category_id: Optional[str] = None
    quantity: Optional[int] = None
    unit_price: Optional[float] = None


@dataclass
class PayerPhone:
    """Payer phone information.

    Attributes:
        area_code: Area or region code. Type: str.
        number: Phone number. Type: str.
    """

    area_code: Optional[str] = None
    number: Optional[str] = None


@dataclass
class PayerAddress:
    """Payer address information.

    Attributes:
        zip_code: Postal code. Type: str.
        street_name: Street name. Type: str.
        street_number: Street number. Type: int.
    """

    zip_code: Optional[str] = None
    street_name: Optional[str] = None
    street_number: Optional[int] = None


@dataclass
class Payer:
    """Payer personal information for fraud scoring.

    Attributes:
        first_name: Payer's first name. Type: str.
        last_name: Payer's last name. Type: str.
        phone: Payer's phone details.
        address: Payer's address details.
    """

    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[PayerPhone] = None
    address: Optional[PayerAddress] = None


@dataclass
class ReceiverAddress:
    """Shipment receiver address.

    Attributes:
        zip_code: Postal code. Type: str.
        street_name: Street name. Type: str.
        street_number: Street number. Type: int.
        floor: Floor or level. Type: str.
        apartment: Apartment or unit. Type: str.
    """

    zip_code: Optional[str] = None
    street_name: Optional[str] = None
    street_number: Optional[int] = None
    floor: Optional[str] = None
    apartment: Optional[str] = None


@dataclass
class Shipments:
    """Shipment information for the payment.

    Attributes:
        receiver_address: Address where the shipment will be delivered.
    """

    receiver_address: Optional[ReceiverAddress] = None


@dataclass
class PaymentAdditionalInfo:
    """Additional information for payment fraud scoring.

    Use this dataclass to build the ``additional_info`` payload when creating
    a payment. Convert to dict with ``dataclasses.asdict()``.

    Attributes:
        items: List of items being purchased.
        payer: Payer personal information.
        shipments: Shipment details.
    """

    items: Optional[List[PaymentItem]] = None
    payer: Optional[Payer] = None
    shipments: Optional[Shipments] = None