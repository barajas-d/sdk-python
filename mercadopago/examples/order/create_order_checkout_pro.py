"""Create a hosted Checkout Pro order through the Orders API."""
from mercadopago import SDK
from mercadopago.config import RequestOptions
from mercadopago.resources.order_checkout_pro import (
    OrderCheckoutProConfig,
    OrderCheckoutProDict,
    OrderCheckoutProInstallments,
    OrderCheckoutProInterestFree,
    OrderCheckoutProOnlineConfig,
    OrderCheckoutProPaymentMethod,
    OrderCheckoutProTrack,
)


def main():
    sdk = SDK("<YOUR_ACCESS_TOKEN>")
    request_options = RequestOptions(
        custom_headers={"x-idempotency-key": "<YOUR_UNIQUE_IDEMPOTENCY_KEY>"}
    )
    order_object = {
        "type": "online",
        "processing_mode": "automatic",
        "capture_mode": "automatic",
        "total_amount": "500.00",
        "external_reference": "ext_ref_checkout_pro",
        "description": "Travel package SAO-RIO with insurance",
        "payer": {"email": "<PAYER_EMAIL>"},
        "transactions": {
            "payments": [
                {
                    "amount": "500.00",
                    "payment_method": {
                        "id": "visa",
                        "type": "credit_card",
                        "token": "<CARD_TOKEN>",
                        "installments": 1,
                    },
                }
            ]
        },
    }

    try:
        response = sdk.order().create(order_object, request_options=request_options)
        order = response["response"]
        print("Order created successfully:")
        print("id:", order.get("id"))
        print("status:", order.get("status"))
        print("status_detail:", order.get("status_detail"))
    except Exception as error:  # pylint: disable=broad-exception-caught
        print("Error:", error)


if __name__ == "__main__":
    main()
