"""Customer address resource for the MercadoPago API.

Wraps ``/v1/customers/{customer_id}/addresses`` endpoints.
"""
from mercadopago.core import MPBase


class CustomerAddress(MPBase):
    """Manages addresses belonging to a customer profile."""

    def list_customer_addresses(self, customer_id, request_options=None):
        """Lists addresses belonging to a customer.

        Args:
            customer_id: Unique customer identifier.
            request_options: Per-call configuration overrides.

        Returns:
            dict: List of customer addresses.
        """
        uri = "/v1/customers/" + self._path_param(customer_id) + "/addresses"
        return self._get(uri=uri, request_options=request_options)

    def update_customer_address(self, customer_id, address_id, address_object,
                                request_options=None):
        """Updates an address belonging to a customer.

        Args:
            customer_id: Unique customer identifier.
            address_id: Unique address identifier.
            address_object: Dict containing updated address fields.
            request_options: Per-call configuration overrides.

        Raises:
            ValueError: If *address_object* is not a ``dict``.

        Returns:
            dict: Updated customer address.
        """
        if not isinstance(address_object, dict):
            raise ValueError("Param address_object must be a Dictionary")

        uri = ("/v1/customers/" + self._path_param(customer_id)
               + "/addresses/" + self._path_param(address_id))
        return self._put(uri=uri, data=address_object,
                         request_options=request_options)

    def create_customer_address(self, customer_id, address_object, request_options=None):
        """Adds an address to a customer profile.

        Args:
            customer_id: Unique customer identifier.
            address_object: Dict containing address fields.
            request_options: Per-call configuration overrides.

        Raises:
            ValueError: If *address_object* is not a ``dict``.

        Returns:
            dict: Created address.
        """
        if not isinstance(address_object, dict):
            raise ValueError("Param address_object must be a Dictionary")

        uri = "/v1/customers/" + self._path_param(customer_id) + "/addresses"
        return self._post(uri=uri, data=address_object, request_options=request_options)

    def delete_customer_address(self, customer_id, address_id, request_options=None):
        """Deletes an address from a customer profile.

        Args:
            customer_id: Unique customer identifier.
            address_id: Unique address identifier.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Deletion confirmation response.
        """
        uri = ("/v1/customers/" + self._path_param(customer_id)
               + "/addresses/" + self._path_param(address_id))
        return self._delete(uri=uri, request_options=request_options)

    def get_customer_address(self, customer_id, address_id, request_options=None):
        """Retrieves a customer's address by its ID.

        Args:
            customer_id: Unique customer identifier.
            address_id: Unique address identifier.
            request_options: Per-call configuration overrides.

        Returns:
            dict: Customer address details.
        """
        uri = ("/v1/customers/" + self._path_param(customer_id)
               + "/addresses/" + self._path_param(address_id))
        return self._get(uri=uri, request_options=request_options)