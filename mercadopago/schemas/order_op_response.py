"""OrderOPResponse schema for Order API operation responses.

Defines the structure of responses returned by order lifecycle operations
such as create, process, capture, cancel, and refund.
"""
from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class OrderOPResponse:
    """Schema for Order API operation responses.

    Represents the standardized response structure returned by the
    MercadoPago Orders API for operations such as order creation,
    processing, capture, cancellation, and refunds.

    Attributes:
        id: Unique order identifier assigned by MercadoPago. Type: str.
        status: Current order status (e.g. ``"created"``, ``"processed"``,
            ``"canceled"``). Type: str.
        type: Order type (e.g. ``"online"``). Type: str.
        processing_mode: Payment processing mode (``"automatic"`` or
            ``"manual"``). Type: str.
        capture_mode: Capture mode (``"automatic"`` or ``"manual"``). Type: str.
        total_amount: Total order amount as a string (e.g. ``"100.00"``).
            Type: str.
        currency: ISO 4217 currency code (e.g. ``"BRL"``, ``"USD"``). Type: str.
        external_reference: Client-provided reference identifier. Type: str.
        marketplace_fee: Marketplace commission amount. Type: str.
        description: Order description provided at creation. Type: str.
        expiration_time: ISO 8601 duration or timestamp for order expiration.
            Type: str.
        checkout_url: URL for Checkout Pro flow when applicable. Type: str.
        date_created: ISO 8601 timestamp when the order was created. Type: str.
        date_last_updated: ISO 8601 timestamp of the most recent update.
            Type: str.
        payer: Payer information dict. Type: dict.
        transactions: Nested dict with ``payments`` and ``refunds`` lists.
            Type: dict.
        items: List of purchased item dicts. Type: list.
        shipment: Shipment details dict. Type: dict.
        config: Configuration options for the order. Type: dict.
        additional_info: Additional metadata supplied by the client. Type: dict.
        metadata: Order-level metadata. Type: dict.
    """

    id: Optional[str] = None
    status: Optional[str] = None
    type: Optional[str] = None
    processing_mode: Optional[str] = None
    capture_mode: Optional[str] = None
    total_amount: Optional[str] = None
    currency: Optional[str] = None
    external_reference: Optional[str] = None
    marketplace_fee: Optional[str] = None
    description: Optional[str] = None
    expiration_time: Optional[str] = None
    checkout_url: Optional[str] = None
    date_created: Optional[str] = None
    date_last_updated: Optional[str] = None
    payer: Optional[Dict[str, Any]] = None
    transactions: Optional[Dict[str, List[Dict[str, Any]]]] = None
    items: Optional[List[Dict[str, Any]]] = None
    shipment: Optional[Dict[str, Any]] = None
    config: Optional[Dict[str, Any]] = None
    additional_info: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None