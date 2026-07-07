from datetime import timedelta

import requests
from django.conf import settings
from django.core.cache import cache
from django.utils import timezone
from django.utils.dateparse import parse_datetime


class NombaAuth:
    BASE_URL = settings.NOMBA_BASE_URL
    CACHE_KEY = "nomba_auth"

    session = requests.Session()

    @classmethod
    def get_token(cls):
        """
        Returns a valid access token.
        If none exists, one is issued.
        If it's close to expiring, it is refreshed.
        """
        auth = cache.get(cls.CACHE_KEY)

        if auth is None:
            return cls._issue_token()

        expires_at = auth["expires_at"]

        # Refresh the token 5 minutes before expiry.
        if timezone.now() >= expires_at - timedelta(minutes=5):
            return cls._refresh_token(auth)

        return auth["access_token"]

    @classmethod
    def _issue_token(cls):
        response = cls.session.post(
            f"{cls.BASE_URL}/auth/token/issue",
            headers=cls._headers(),
            json={
                "grant_type": "client_credentials",
                "client_id": settings.NOMBA_CLIENT_ID,
                "client_secret": settings.NOMBA_CLIENT_SECRET,
            },
        )

        response.raise_for_status()

        data = response.json()["data"]

        cls._save_tokens(data)

        return data["access_token"]

    @classmethod
    def _refresh_token(cls, auth):
        response = cls.session.post(
            f"{cls.BASE_URL}/auth/token/refresh",
            headers={
                **cls._headers(),
                "Authorization": f"Bearer {auth['access_token']}",
            },
            json={
                "grant_type": "refresh_token",
                "refresh_token": auth["refresh_token"],
            },
        )

        # If refresh fails (expired refresh token, revoked, etc.)
        # simply issue a brand new token.
        if not response.ok:
            return cls._issue_token()

        data = response.json()["data"]

        cls._save_tokens(data)

        return data["access_token"]

    @classmethod
    def _save_tokens(cls, data):
        auth = {
            "access_token": data["access_token"],
            "refresh_token": data["refresh_token"],
            "expires_at": parse_datetime(data["expiresAt"]),
        }

        # Cache indefinitely. We determine validity ourselves
        # using expires_at.
        cache.set(cls.CACHE_KEY, auth, timeout=None)

    @staticmethod
    def _headers():
        return {
            "Content-Type": "application/json",
            "accountId": settings.NOMBA_ACCOUNT_ID,
        }