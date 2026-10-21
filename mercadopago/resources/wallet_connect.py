"""Wallet Connect resource for agreements, payer tokens, coupons and discounts."""
from copy import copy

from mercadopago.core import MPBase


class WalletConnect(MPBase):
    """Manages the Wallet Connect authorization and discount flow."""

    def get_wallet_agreement(self, agreement_id, params=None, request_options=None):
        """Retrieves a Wallet Connect agreement by its identifier.

        Args:
            agreement_id: Identifier of the agreement to retrieve.
            params: Optional query parameters, such as ``client.id``.
            request_options: Per-call options; use platform_id for x-platform-id.

        Returns:
            dict: HTTP status and agreement response.
        """
        if params is not None and not isinstance(params, dict):
            raise ValueError("Param params must be a Dictionary")
        uri = "/v2/wallet_connect/agreements/" + self._path_param(agreement_id)
        return self._get(uri=uri, filters=params, request_options=request_options)

    def delete_wallet_agreement(self, agreement_id, params=None, request_options=None):
        """Revokes a Wallet Connect agreement.

        Args:
            agreement_id: Identifier of the agreement to revoke.
            params: Optional query parameters, such as ``client.id``.
            request_options: Per-call options; use platform_id for x-platform-id.

        Returns:
            dict: HTTP status and revocation response.
        """
        if params is not None and not isinstance(params, dict):
            raise ValueError("Param params must be a Dictionary")
        uri = "/v2/wallet_connect/agreements/" + self._path_param(agreement_id)
        return self._delete(uri=uri, params=params, request_options=request_options)

    def create_wallet_agreement(self, agreement_object, params=None, request_options=None):
        """Creates an agreement for wallet authorization.

        Args:
            agreement_object: Request body with return_uri and external_flow_id;
                may also contain agreement_data and external_user.
            params: Optional query parameters, such as ``client.id``.
            request_options: Per-call options; use platform_id for x-platform-id.

        Returns:
            dict: HTTP status and agreement response.
        """
        if not isinstance(agreement_object, dict):
            raise ValueError("Param agreement_object must be a Dictionary")
        if params is not None and not isinstance(params, dict):
            raise ValueError("Param params must be a Dictionary")
        return self._post(uri="/v2/wallet_connect/agreements", data=agreement_object,
                          params=params, request_options=request_options)

    def create_wallet_payer_token(self, agreement_id, token_object, request_options=None):
        """Exchanges an authorization code for a payer token.

        Args:
            agreement_id: Identifier of the authorized agreement.
            token_object: Request body containing the authorization ``code``.
            request_options: Per-call options; use platform_id for x-platform-id.

        Returns:
            dict: HTTP status and payer token response.
        """
        if not isinstance(token_object, dict):
            raise ValueError("Param token_object must be a Dictionary")
        uri = ("/v2/wallet_connect/agreements/" + self._path_param(agreement_id)
               + "/payer_token")
        return self._post(uri=uri, data=token_object,
                          request_options=request_options)

    def validate_wallet_coupon(self, coupon_object, payer_token, request_options=None):
        """Validates a wallet coupon using the payer's token.

        Args:
            coupon_object: Request body containing the coupon ``id``.
            payer_token: Required x-payer-token header value.
            request_options: Per-call configuration overrides.

        Returns:
            dict: HTTP status and coupon validation response.
        """
        if not isinstance(coupon_object, dict):
            raise ValueError("Param coupon_object must be a Dictionary")
        options = copy(request_options if request_options is not None else self.request_options)
        options.custom_headers = dict(options.custom_headers or {}, **{"x-payer-token": payer_token})
        return self._post(uri="/v2/wallet_connect/coupons", data=coupon_object,
                          request_options=options)

    def create_wallet_discount(self, discount_object, payer_token, request_options=None):
        """Creates a discount promise for the given coupon and amount.

        Args:
            discount_object: Request body with ``coupon`` and ``amount``.
            payer_token: Required x-payer-token header value.
            request_options: Per-call configuration overrides.

        Returns:
            dict: HTTP status and discount promise response.
        """
        if not isinstance(discount_object, dict):
            raise ValueError("Param discount_object must be a Dictionary")
        options = copy(request_options if request_options is not None else self.request_options)
        options.custom_headers = dict(options.custom_headers or {}, **{"x-payer-token": payer_token})
        return self._post(uri="/v2/wallet_connect/discounts", data=discount_object,
                          request_options=options)