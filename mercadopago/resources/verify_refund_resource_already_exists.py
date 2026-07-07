"""Refund resource verification and usage documentation.

This module serves as documentation confirming that the Refund resource already
exists in the MercadoPago Python SDK at `mercadopago/resources/refund.py`.

The existing :class:`~mercadopago.resources.refund.Refund` resource provides:

1. **list_all(payment_id, request_options=None)**
   Lists all refunds issued for a given payment.

   Example::

       refunds = sdk.refund().list_all(payment_id="123456789")

2. **create(payment_id, refund_object=None, request_options=None)**
   Creates a full or partial refund for a payment.

   - **Full refund**: Omit `refund_object` or pass `None`.
   - **Partial refund**: Pass `{"amount": <float>}`.

   Example (full refund)::

       result = sdk.refund().create(payment_id="123456789")

   Example (partial refund)::

       result = sdk.refund().create(
           payment_id="123456789",
           refund_object={"amount": 25.50}
       )

**Additional refund functionality:**

For advanced (split) payment disbursements, see the
:class:`~mercadopago.resources.disbursement_refund.DisbursementRefund` resource
located at `mercadopago/resources/disbursement_refund.py`. It provides:

- **list_all(advanced_payment_id)**: Lists refunds for an advanced payment.
- **create_all(advanced_payment_id, disbursement_refund_object)**: Refunds all
  disbursements.
- **create(advanced_payment_id, disbursement_id, amount)**: Refunds a specific
  disbursement by amount.
- **save(advanced_payment_id, disbursement_id, disbursement_refund_object)**:
  Creates a disbursement refund with a custom payload.

**Order refunds:**

The :class:`~mercadopago.resources.order.Order` resource at
`mercadopago/resources/order.py` provides order-level refund methods:

- **refund_transaction(order_id, transaction_object=None)**: Refunds transactions
  within an order. Pass `None` for full refund or a dict with `"amount"` for
  partial refund.
- **refund(order_id, refund_object=None)**: Alias for `refund_transaction`.

**Summary:**

No new Refund resource implementation is required. All refund operations are
already available through:

1. :class:`~mercadopago.resources.refund.Refund` for payment refunds.
2. :class:`~mercadopago.resources.disbursement_refund.DisbursementRefund` for
   advanced payment disbursement refunds.
3. :class:`~mercadopago.resources.order.Order` for order transaction refunds.

**API References:**

- Payment Refunds: https://www.mercadopago.com/developers/en/reference/online-payments/checkout-api-payments/create-refund/post
- Advanced Payment Refunds: https://www.mercadopago.com/developers/en/reference (advanced_payments section)
- Order Refunds: https://www.mercadopago.com/developers/en/reference/online-payments/checkout-api/refund-order/post
"""

# This module intentionally contains no executable code.
# It exists solely to document that refund functionality is already implemented.