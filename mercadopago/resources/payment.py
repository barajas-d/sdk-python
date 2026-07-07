"""Payment resource for the MercadoPago Checkout API.

Wraps ``/v1/payments`` endpoints to search, retrieve, create, update, and
capture payments.

`API reference <https://www.mercadopago.com/developers/en/reference/online-payments/checkout-api-payments/create-payment/post>`_
"""
from mercadopago.core import MPBase


class Payment(MPBase):
    """Manages payment lifecycle through the MercadoPago Checkout API.

    Supports transparent (server-to-server) payments as well as payments
    originated from Checkout Pro / Checkout Bricks. Enables capture, refund,
    and cancellation operations on existing payments.

    `Integration guide
    <https://www.mercadopago.com.br/developers/en/guides/online-payments/checkout-api/introduction/>`_
    """

    def search(self, filters=None, request_options=None):
        """Searches payments matching the given filters.

        Args:
            filters: Query-string parameters such as ``external_reference``,
                ``status``, ``date_created``, ``payer.id``, ``offset``,
                ``limit``, etc.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Paginated list of matching payments with ``paging`` metadata.

        Reference: https://www.mercadopago.com/developers/en/reference/online-payments/checkout-api-payments/search-payments/get
        """
        return self._get(uri="/v1/payments/search", filters=filters,
                         request_options=request_options)

    def get(self, payment_id, request_options=None):
        """Retrieves a single payment by its ID.

        Args:
            payment_id: Numeric or string payment identifier.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Full payment object including status, amounts, payer details,
                and transaction metadata.

        Reference: https://www.mercadopago.com/developers/en/reference/online-payments/checkout-api-payments/get-payment/get
        """
        return self._get(uri="/v1/payments/" + str(payment_id), request_options=request_options)

    def create(self, payment_object, request_options=None):
        """Creates a new payment.

        Args:
            payment_object: Dict describing the payment. Must include
                ``transaction_amount``, ``payment_method_id``, and ``payer``.
                Common fields include:

                - ``token``: Card token for credit/debit card payments.
                - ``installments``: Number of installments (default 1).
                - ``description``: Payment description.
                - ``external_reference``: Merchant's payment reference.
                - ``statement_descriptor``: Text shown on card statement.
                - ``capture``: ``False`` for two-step (auth-only) payments.
                - ``binary_mode``: ``True`` for instant approval/rejection.
                - ``notification_url``: Webhook endpoint for payment updates.
                - ``callback_url``: Redirect URL after bank authorization (e.g. PSE).
                - ``additional_info``: Metadata with items, payer, and shipment details.

            request_options: Per-call configuration overrides.

        Raises:
            ValueError: If *payment_object* is not a ``dict``.

        Returns:
            dict: Created payment including ``id``, ``status``,
                ``status_detail``, and (when applicable) ``point_of_interaction``
                with redirect URLs or QR code data.

        Reference: https://www.mercadopago.com/developers/en/reference/online-payments/checkout-api-payments/create-payment/post
        """
        if not isinstance(payment_object, dict):
            raise ValueError("Param payment_object must be a Dictionary")

        return self._post(uri="/v1/payments", data=payment_object, request_options=request_options)

    def update(self, payment_id, payment_object, request_options=None):
        """Updates an existing payment.

        Commonly used to change ``status`` (e.g. ``"cancelled"``) or update
        metadata. Not all fields are mutable; refer to the API reference for
        details on which attributes can be modified post-creation.

        Args:
            payment_id: Identifier of the payment to update.
            payment_object: Dict with the fields to modify (e.g. ``status``,
                ``additional_info``, ``capture``).
            request_options: Per-call configuration overrides.

        Raises:
            ValueError: If *payment_object* is not a ``dict``.

        Returns:
            dict: Updated payment object.

        Reference: https://www.mercadopago.com/developers/en/reference/online-payments/checkout-api-payments/update-payment/put
        """
        if not isinstance(payment_object, dict):
            raise ValueError("Param payment_object must be a Dictionary")

        return self._put(uri="/v1/payments/" + str(payment_id), data=payment_object,
                         request_options=request_options)

    def cancel(self, payment_id, request_options=None):
        """Cancels a payment.

        Sends a PUT request with ``{"status": "cancelled"}`` to cancel an
        approved or pending payment. Only payments that have not yet been
        captured or settled can be cancelled.

        Args:
            payment_id: Identifier of the payment to cancel.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Cancelled payment with ``status`` set to ``"cancelled"``.

        Reference: https://www.mercadopago.com/developers/en/reference/online-payments/checkout-api-payments/update-payment/put
        """
        cancel_object = {"status": "cancelled"}
        return self._put(uri="/v1/payments/" + str(payment_id), data=cancel_object,
                         request_options=request_options)

    def capture(self, payment_id, amount=None, request_options=None):
        """Captures a previously authorized payment.

        Used in two-step payment flows where the payment was created with
        ``capture=False``. Sends a PUT request with ``{"capture": True}`` to
        settle the funds.

        Args:
            payment_id: Identifier of the payment to capture.
            amount: Optional partial capture amount. If ``None``, the full
                authorized amount is captured.
            request_options: Per-call configuration overrides.

        Raises:
            ValueError: If *amount* is provided but not a ``float`` or ``int``.

        Returns:
            dict: Captured payment with updated ``status`` and amounts.

        Reference: https://www.mercadopago.com/developers/en/reference/online-payments/checkout-api-payments/update-payment/put
        """
        if amount is not None and not isinstance(amount, (int, float)):
            raise ValueError("Param amount must be a number (int or float)")

        capture_object = {"capture": True}
        if amount is not None:
            capture_object["transaction_amount"] = float(amount)

        return self._put(uri="/v1/payments/" + str(payment_id), data=capture_object,
                         request_options=request_options)