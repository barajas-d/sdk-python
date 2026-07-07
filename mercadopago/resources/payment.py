"""Payment resource for the MercadoPago Checkout API.

Wraps ``/v1/payments`` endpoints to search, retrieve, create, update, and
cancel payments.

`API reference <https://www.mercadopago.com/developers/en/reference/online-payments/checkout-api-payments/create-payment/post>`_
"""
from mercadopago.core import MPBase


class Payment(MPBase):
    """Manages payment lifecycle through the MercadoPago Checkout API.

    Supports transparent (server-to-server) payments as well as payments
    originated from Checkout Pro / Checkout Bricks.

    `Integration guide
    <https://www.mercadopago.com.br/developers/en/guides/online-payments/checkout-api/introduction/>`_
    """

    def search(self, filters=None, request_options=None):
        """Searches payments matching the given filters.

        Args:
            filters: Query-string parameters such as ``external_reference``,
                ``status``, ``date_created``, ``begin_date``, ``end_date``,
                ``limit``, ``offset``, etc.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Paginated list of matching payments with ``paging`` and
                ``results`` keys.

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
            dict: Full payment object including status, amounts, payer
                information, payment method details, and timestamps.

        Reference: https://www.mercadopago.com/developers/en/reference/online-payments/checkout-api-payments/get-payment/get
        """
        return self._get(uri="/v1/payments/" + str(payment_id), request_options=request_options)

    def create(self, payment_object, request_options=None):
        """Creates a new payment.

        Args:
            payment_object: Dict describing the payment with the following
                typical fields:

                - ``transaction_amount`` (float): Payment amount.
                - ``payment_method_id`` (str): Payment method (e.g. ``"pix"``,
                  ``"visa"``, ``"master"``).
                - ``token`` (str): Card token for credit/debit card payments
                  (obtained via Card Token API or JS SDK).
                - ``installments`` (int): Number of installments (default 1).
                - ``payer`` (dict): Payer information including ``email``,
                  ``identification``, ``first_name``, ``last_name``, etc.
                - ``description`` (str): Payment description.
                - ``external_reference`` (str): Your internal reference ID.
                - ``statement_descriptor`` (str): Text shown on card statement.
                - ``capture`` (bool): Whether to capture immediately (default
                  ``True``). Set to ``False`` for two-step flows.
                - ``binary_mode`` (bool): When ``True``, payment can only be
                  approved or rejected (no pending states).
                - ``notification_url`` (str): Webhook URL for payment updates.
                - ``callback_url`` (str): Redirect URL after payment (for
                  redirect-based methods like PIX or bank transfers).
                - ``additional_info`` (dict): Extra metadata such as items,
                  payer details, and shipment information.

            request_options: Per-call configuration overrides.

        Raises:
            ValueError: If *payment_object* is not a ``dict``.

        Returns:
            dict: Created payment including ``id``, ``status``,
                ``status_detail``, and additional processing information.
                For redirect-based methods (e.g. PIX), includes
                ``point_of_interaction`` with QR code or redirect URL.

        Reference: https://www.mercadopago.com/developers/en/reference/online-payments/checkout-api-payments/create-payment/post
        """
        if not isinstance(payment_object, dict):
            raise ValueError("Param payment_object must be a Dictionary")

        return self._post(uri="/v1/payments", data=payment_object, request_options=request_options)

    def update(self, payment_id, payment_object, request_options=None):
        """Updates an existing payment.

        Commonly used to change ``status`` (e.g. cancel) or update
        metadata on a payment that has not yet been captured.

        Args:
            payment_id: Identifier of the payment to update.
            payment_object: Dict with the fields to modify. Common fields
                include:

                - ``status`` (str): New payment status (e.g. ``"cancelled"``).
                - ``capture`` (bool): Set to ``True`` to capture a previously
                  authorized payment.
                - ``transaction_amount`` (float): Update amount (only for
                  uncaptured payments).

            request_options: Per-call configuration overrides.

        Raises:
            ValueError: If *payment_object* is not a ``dict``.

        Returns:
            dict: Updated payment object with the modified fields.

        Reference: https://www.mercadopago.com/developers/en/reference/online-payments/checkout-api-payments/update-payment/put
        """
        if not isinstance(payment_object, dict):
            raise ValueError("Param payment_object must be a Dictionary")

        return self._put(uri="/v1/payments/" + str(payment_id), data=payment_object,
                         request_options=request_options)

    def cancel(self, payment_id, request_options=None):
        """Cancels a payment.

        Sets the payment status to ``cancelled``. Only pending or
        in_process payments can be cancelled. For authorized (uncaptured)
        payments, use :meth:`update` with ``{"status": "cancelled"}``.

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

    def capture(self, payment_id, request_options=None):
        """Captures a previously authorized payment.

        Use this for two-step payment flows where the payment was created
        with ``capture=False``. Sends ``{"capture": true}`` to finalize
        the transaction.

        Args:
            payment_id: Identifier of the payment to capture.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Captured payment with updated ``status`` and amounts.

        Reference: https://www.mercadopago.com/developers/en/reference/online-payments/checkout-api-payments/update-payment/put
        """
        capture_object = {"capture": True}
        return self._put(uri="/v1/payments/" + str(payment_id), data=capture_object,
                         request_options=request_options)