"""Subscription resource for the MercadoPago Subscriptions API.

Wraps ``/preapproval`` endpoints to search, retrieve, create, and update
plan-based subscriptions.  A subscription links a payer to a
:class:`~mercadopago.resources.plan.Plan` template for recurring billing.

`API reference
<https://www.mercadopago.com/developers/en/reference/online-payments/subscriptions/create-preapproval/post>`_
"""
from mercadopago.core import MPBase


class Subscription(MPBase):
    """Manages plan-based recurring subscriptions.

    Each subscription is associated with a :class:`Plan` that defines
    billing frequency and amount.  Use :meth:`create` with a
    ``preapproval_plan_id`` to subscribe a payer to an existing plan.
    Subscriptions can also be created without a plan by providing
    ``auto_recurring`` configuration directly.
    """

    def search(self, filters=None, request_options=None):
        """Searches subscriptions matching the given filters.

        Args:
            filters: Query-string parameters (e.g. ``status``,
                ``preapproval_plan_id``, ``payer_email``).
            request_options: Per-call configuration overrides.

        Returns:
            dict: Paginated list of matching subscriptions with ``results``
                and ``paging`` metadata.

        Reference: https://www.mercadopago.com/developers/en/reference/online-payments/subscriptions/search-preapproval/get
        """
        return self._get(
            uri="/preapproval/search",
            filters=filters,
            request_options=request_options)

    def get(self, subscription_id, request_options=None):
        """Retrieves a subscription by its ID.

        Args:
            subscription_id: Unique subscription identifier.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Full subscription object including ``id``, ``status``,
                ``payer_email``, ``auto_recurring`` configuration, and
                payment details.

        Reference: https://www.mercadopago.com/developers/en/reference/online-payments/subscriptions/get-preapproval/get
        """
        return self._get(
            uri="/preapproval/" + str(subscription_id),
            request_options=request_options)

    def create(self, subscription_object, request_options=None):
        """Creates a new subscription.

        Subscriptions can be created either:
        - With a plan: Include ``preapproval_plan_id`` to use an existing
          :class:`Plan` template.
        - Without a plan: Provide ``auto_recurring`` configuration directly
          in the request.

        Required fields:
        - ``reason``: Subscription description
        - ``payer_email``: Subscriber's email
        - ``back_url``: Return URL after subscription flow
        - ``auto_recurring``: Billing configuration (frequency,
          frequency_type, transaction_amount, currency_id)
        - ``card_token_id``: Payment method token (for authorized status)

        Optional fields:
        - ``preapproval_plan_id``: Link to existing plan
        - ``external_reference``: Your internal identifier
        - ``status``: Initial status (``"authorized"`` requires card_token_id)

        Args:
            subscription_object: Dict defining the subscription
                (preapproval_plan_id, payer_email, card_token_id,
                auto_recurring, reason, back_url, etc.).
            request_options: Per-call configuration overrides.

        Raises:
            ValueError: If *subscription_object* is not a ``dict``.

        Returns:
            dict: Created subscription including its ``id``, ``status``,
                and ``init_point`` (redirect URL for subscriber to complete
                payment method setup).

        Reference: https://www.mercadopago.com/developers/en/reference/online-payments/subscriptions/create-preapproval/post
        """
        if not isinstance(subscription_object, dict):
            raise ValueError("Param subscription_object must be a Dictionary")

        return self._post(
            uri="/preapproval",
            data=subscription_object,
            request_options=request_options)

    def update(self, subscription_id, subscription_object, request_options=None):
        """Updates an existing subscription.

        Commonly used to:
        - Change status (``"paused"``, ``"authorized"``, ``"cancelled"``)
        - Update payment method via new ``card_token_id``
        - Modify ``auto_recurring`` configuration
        - Update ``reason`` or ``external_reference``

        Args:
            subscription_id: Identifier of the subscription to update.
            subscription_object: Dict with the fields to modify.
            request_options: Per-call configuration overrides.

        Raises:
            ValueError: If *subscription_object* is not a ``dict``.

        Returns:
            dict: Updated subscription object with new field values.

        Reference: https://www.mercadopago.com/developers/en/reference/online-payments/subscriptions/update-preapproval/put
        """
        if not isinstance(subscription_object, dict):
            raise ValueError("Param subscription_object must be a Dictionary")

        return self._put(
            uri="/preapproval/" + str(subscription_id),
            data=subscription_object,
            request_options=request_options)