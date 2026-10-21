"""Customer address resource for the MercadoPago API.

Wraps the ``/v1/customers/{customer_id}/addresses`` endpoints.
"""
from urllib.parse import quote

from mercadopago.core import MPBase


class CustomerAddress(MPBase):
    """Manages addresses associated with a customer profile."""

    @staticmethod
    def _path_param(value):
        """Encode one path parameter without allowing embedded path separators."""
        return quote(str(value), safe="")

    def list_customer_addresses(self, customer_id, request_options=None):
        """Lists addresses associated with a customer.

        Args:
            customer_id: Identifier of the customer.
            request_options: Per-call configuration overrides.

        Returns:
            dict: List of customer addresses and HTTP status.
        """
        return self._get(
            uri=f"/v1/customers/{self._path_param(customer_id)}/addresses",
            request_options=request_options,
        )

    def create_customer_address(self, customer_id, address_object, request_options=None):
        """Creates an address associated with a customer.

        Args:
            customer_id: Identifier of the customer.
            address_object: Dictionary containing the address to create.
            request_options: Per-call configuration overrides.

        Raises:
            ValueError: If *address_object* is not a dictionary.

        Returns:
            dict: Created address and HTTP status.
        """
        if not isinstance(address_object, dict):
            raise ValueError("Param address_object must be a Dictionary")

        return self._post(
            uri=f"/v1/customers/{self._path_param(customer_id)}/addresses",
            data=address_object,
            request_options=request_options,
        )

    def delete_customer_address(self, customer_id, address_id, request_options=None):
        """Deletes an address from a customer profile.

        Args:
            customer_id: Identifier of the customer.
            address_id: Identifier of the address to delete.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Deletion response and HTTP status.
        """
        return self._delete(
            uri=f"/v1/customers/{self._path_param(customer_id)}/addresses/"
                f"{self._path_param(address_id)}",
            request_options=request_options,
        )

    def update_customer_address(self, customer_id, address_id, address_object, request_options=None):
        """Updates an address associated with a customer.

        Args:
            customer_id: Identifier of the customer.
            address_id: Identifier of the address to update.
            address_object: Dictionary containing address fields to update.
            request_options: Per-call configuration overrides.

        Raises:
            ValueError: If *address_object* is not a dictionary.

        Returns:
            dict: Updated customer address and HTTP status.
        """
        if not isinstance(address_object, dict):
            raise ValueError("Param address_object must be a Dictionary")

        return self._put(
            uri=f"/v1/customers/{self._path_param(customer_id)}/addresses/"
                f"{self._path_param(address_id)}",
            data=address_object,
            request_options=request_options,
        )

    def get_customer_address(self, customer_id, address_id, request_options=None):
        """Retrieves an address from a customer profile.

        Args:
            customer_id: Identifier of the customer.
            address_id: Identifier of the address to retrieve.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Customer address and HTTP status.
        """
        return self._get(
            uri=f"/v1/customers/{self._path_param(customer_id)}/addresses/"
                f"{self._path_param(address_id)}",
            request_options=request_options,
        )