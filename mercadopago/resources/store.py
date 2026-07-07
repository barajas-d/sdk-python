"""Store resource for the MercadoPago API.

Wraps ``/v1/stores`` endpoints to manage physical or virtual store locations
associated with a MercadoPago account.  Stores can be linked to Point devices
and used to organize transactions by location.

`API reference
<https://www.mercadopago.com/developers/en/reference>`_
"""
from mercadopago.core import MPBase


class Store(MPBase):
    """Manages store locations for Point devices and transaction organization.

    Stores represent physical or virtual locations where payments are
    processed.  Each store can be associated with one or more Point
    devices and helps organize transactions by location.
    """

    def list_all(self, filters=None, request_options=None):
        """Lists all stores for the authenticated account.

        Args:
            filters: Optional query-string parameters (e.g. ``external_id``).
            request_options: Per-call configuration overrides.

        Returns:
            dict: List of store objects.

        Reference: https://www.mercadopago.com/developers/en/reference
        """
        return self._get(
            uri="/v1/stores",
            filters=filters,
            request_options=request_options,
        )

    def get(self, store_id, request_options=None):
        """Retrieves a store by its ID.

        Args:
            store_id: Unique store identifier.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Full store object including location and business hours.

        Reference: https://www.mercadopago.com/developers/en/reference
        """
        return self._get(
            uri=f"/v1/stores/{str(store_id)}",
            request_options=request_options,
        )

    def create(self, store_object, request_options=None):
        """Creates a new store.

        Args:
            store_object: Dict with store data (name, location, business_hours,
                external_id, etc.).
            request_options: Per-call configuration overrides.

        Raises:
            ValueError: If *store_object* is not a ``dict``.

        Returns:
            dict: Created store including its ``id``.

        Reference: https://www.mercadopago.com/developers/en/reference
        """
        if not isinstance(store_object, dict):
            raise ValueError("Param store_object must be a Dictionary")

        return self._post(
            uri="/v1/stores",
            data=store_object,
            request_options=request_options,
        )

    def update(self, store_id, store_object, request_options=None):
        """Updates an existing store.

        Args:
            store_id: Identifier of the store to update.
            store_object: Dict with the fields to modify.
            request_options: Per-call configuration overrides.

        Raises:
            ValueError: If *store_object* is not a ``dict``.

        Returns:
            dict: Updated store object.

        Reference: https://www.mercadopago.com/developers/en/reference
        """
        if not isinstance(store_object, dict):
            raise ValueError("Param store_object must be a Dictionary")

        return self._put(
            uri=f"/v1/stores/{str(store_id)}",
            data=store_object,
            request_options=request_options,
        )

    def delete(self, store_id, request_options=None):
        """Deletes a store.

        Args:
            store_id: Identifier of the store to delete.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Deletion confirmation response.

        Reference: https://www.mercadopago.com/developers/en/reference
        """
        return self._delete(
            uri=f"/v1/stores/{str(store_id)}",
            request_options=request_options,
        )