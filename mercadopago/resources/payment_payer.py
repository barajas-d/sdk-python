"""PaymentPayer schema for the MercadoPago Payments API.

Defines the :class:`PaymentPayer` data model representing the payer
(buyer) in a payment request.  This is a data class intended for use
within payment objects sent to the Payments API.
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class PaymentPayerIdentification:
    """Identification document of the payer.

    Attributes:
        type: Document type code (e.g. ``"CPF"``, ``"CNPJ"``, ``"DNI"``).
            Type: str.
        number: Document number as a string. Type: str.
    """

    type: Optional[str] = None
    number: Optional[str] = None


@dataclass
class PaymentPayer:
    """Payer (buyer) information for a payment request.

    Use this dataclass to build the ``payer`` payload when creating a
    payment through the Payments API. Convert to dict with
    ``dataclasses.asdict()``.

    Attributes:
        email: Payer's email address. **Required**. Type: str.
        id: MercadoPago user ID of the payer, when available. Type: str.
        identification: Payer's identification document details.
        type: Payer type. One of ``"customer"`` (registered buyer),
            ``"registered"`` (MercadoPago user who is not a saved
            customer), or ``"guest"`` (unregistered buyer). Type: str.
    """

    email: str
    id: Optional[str] = None
    identification: Optional[PaymentPayerIdentification] = None
    type: Optional[str] = None