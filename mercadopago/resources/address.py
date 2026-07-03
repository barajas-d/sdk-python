"""Address data model for MercadoPago API requests.

Defines the :class:`Address` dataclass representing physical addresses in
payer, shipment, and other contexts. This is a plain data model and does not
extend :class:`~mercadopago.core.mp_base.MPBase`.
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Address:
    """Physical address data model.

    Use this dataclass to build address payloads for payer, shipment, or
    other address fields in order and payment requests. Convert to dict with
    ``dataclasses.asdict()``.

    Attributes:
        city: City name. Type: str, optional.
        country: Country code (e.g. ``"BR"``, ``"AR"``). Type: str, optional.
        state: State or province name. Type: str, optional.
        street_name: Street name without number. Type: str, optional.
        street_number: Street number. Type: str, optional.
        zip_code: Postal code. Type: str, optional.
    """

    city: Optional[str] = None
    country: Optional[str] = None
    state: Optional[str] = None
    street_name: Optional[str] = None
    street_number: Optional[str] = None
    zip_code: Optional[str] = None