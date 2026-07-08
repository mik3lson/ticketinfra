import requests

from .auth import NombaAuth
from django.conf import settings


class NombaClient:
    BASE_URL = settings.NOMBA_BASE_URL

    @classmethod
    def request(cls, method, endpoint, **kwargs):
        token = NombaAuth.get_token()

        headers = kwargs.pop("headers", {})

        headers.update(
            {
                "Authorization": f"Bearer {token}",
                "accountId": "{settings.NOMBA_ACCOUNT_ID}",
                "Content-Type": "application/json",
            }
        )

        response = requests.request(
            method,
            cls.BASE_URL + endpoint,
            headers=headers,
            **kwargs,
        )

        response.raise_for_status()

        return response.json()