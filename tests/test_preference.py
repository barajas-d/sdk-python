"""
    Module: test_preference
"""
import os
import unittest
import time
import mercadopago
from mercadopago.http import HttpClient


class FakeHttpClient(HttpClient):
    """Captures PUT requests without sending them to the API."""

    def __init__(self):
        self.put_calls = []
        self.response = {
            "status": 200,
            "response": {"id": 123, "expires": True},
        }

    def put(self, url, headers, data=None, params=None, timeout=None, maxretries=None):
        self.put_calls.append({
            "url": url,
            "headers": headers,
            "data": data,
            "params": params,
            "timeout": timeout,
            "maxretries": maxretries,
        })
        return self.response


class TestPreference(unittest.TestCase):
    """
    Test Module: Preference
    """
    sdk = mercadopago.SDK(os.environ['ACCESS_TOKEN'])

    def test_all(self):
        """
        Test Module: Preference
        """
        preference_object = {
            "items": [
                {
                    "description": "Test Update Success",
                    "id": "456",
                    "picture_url": "http://product1.image.png",
                    "quantity": 1,
                    "title": "Item 1",
                    "currency_id": "BRL",
                    "unit_price": 20.5
                }
            ]
        }
        preference_saved = self.sdk.preference().create(preference_object)
        self.assertEqual(preference_saved["status"], 201)
        time.sleep(3)

        preference_object["items"][0]["title"] = "Testando 1 2 3"

        preference_id = preference_saved["response"]["id"]
        preference_update = self.sdk.preference().update(preference_id, preference_object)
        self.assertEqual(preference_update["status"], 200)

        time.sleep(3)
        preference_saved = self.sdk.preference().get(preference_id)
        self.assertEqual(preference_saved["status"], 200)
        self.assertEqual(preference_saved["response"]["items"][0]["title"],
                         preference_object["items"][0]["title"])

        time.sleep(3)
        preference_search = self.sdk.preference().search()
        self.assertEqual(preference_search["status"], 200)

    def test_expire_uses_put_endpoint_and_propagates_response(self):
        """Test expiring a preference through its dedicated endpoint."""
        http_client = FakeHttpClient()
        preference = mercadopago.SDK(
            "TEST_ACCESS_TOKEN", http_client=http_client
        ).preference()

        response = preference.expire(123)

        self.assertIs(response, http_client.response)
        self.assertEqual(len(http_client.put_calls), 1)
        self.assertEqual(
            http_client.put_calls[0]["url"],
            "https://api.mercadopago.com/checkout/preferences/123/expire",
        )


if __name__ == "__main__":
    unittest.main()
