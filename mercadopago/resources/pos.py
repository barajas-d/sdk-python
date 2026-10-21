"""Point of Sale resource for the MercadoPago API.

Wraps the ``/pos`` endpoint to search points of sale.
"""
from mercadopago.core import MPBase


class POS(MPBase):
    """Searches points of sale belonging to the authenticated seller."""

    def create_pos(self, pos_object, request_options=None):
        """Creates a point of sale with its own QR code.

        Args:
            pos_object: POSRequest dict with ``name`` and ``store_id``.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Created point of sale and HTTP status.
        """
        if not isinstance(pos_object, dict):
            raise ValueError("Param pos_object must be a Dictionary")

        return self._post(uri="/pos", data=pos_object,
                          request_options=request_options)

    def list_pos(self, user_id, request_options=None):
        """Lists points of sale for a user.

        Args:
            user_id: Identifier of the user whose points of sale are listed.
            request_options: Per-call configuration overrides.

        Returns:
            dict: List of points of sale and HTTP status.
        """
        return self._get(uri="/users/" + self._path_param(user_id) + "/pos",
                         filters=None, request_options=request_options)

    def search_pos(self, filters=None, request_options=None):
        """Searches points of sale using optional query filters.

        Args:
            filters: Query parameters such as ``external_id``,
                ``external_store_id``, ``store_id``, and ``category``.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Paginated search results with ``paging`` and ``results``.
        """
        if filters is not None and not isinstance(filters, dict):
            raise ValueError("Param filters must be a Dictionary")

        return self._get(uri="/pos", filters=filters,
                         request_options=request_options)

    def get_pos(self, id, request_options=None):
        """Retrieves a point of sale by its identifier.

        Args:
            id: Identifier of the point of sale to retrieve.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Point of sale details and HTTP status.
        """
        return self._get(uri="/pos/" + self._path_param(id),
                         request_options=request_options)

    def update_pos(self, id, pos_object, request_options=None):
        """Updates a point of sale by its identifier.

        Args:
            id: Identifier of the point of sale to update.
            pos_object: POSRequest dict with the updated POS details.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Updated point of sale and HTTP status.
        """
        if not isinstance(pos_object, dict):
            raise ValueError("Param pos_object must be a Dictionary")

        return self._put(uri="/pos/" + self._path_param(id),
                         data=pos_object, request_options=request_options)

    @staticmethod
    def _path_param(value):
        """Escapes an identifier as a single URL path segment.

        Args:
            value: Path parameter to encode.

        Returns:
            str: Percent-encoded path parameter.
        """
        from urllib.parse import quote

        return quote(str(value), safe="")

    def delete_pos(self, id, request_options=None):
        """Deletes a point of sale by its identifier.

        Args:
            id: Identifier of the point of sale to delete.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Deletion response and HTTP status.
        """
        return self._delete(uri="/pos/" + self._path_param(id),
                            request_options=request_options)
