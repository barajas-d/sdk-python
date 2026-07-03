"""Phone data model for the MercadoPago API.

Represents phone number information used in payer, customer, and other
resources. This is a simple data structure, not a resource endpoint.
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Phone:
    """Phone number information.

    Used to represent phone contact details in various API requests and
    responses. Both fields are optional.

    Attributes:
        area_code: Phone area code (e.g. "11" for São Paulo). Type: str.
        number: Phone number without area code. Type: str.
    """

    area_code: Optional[str] = None
    number: Optional[str] = None