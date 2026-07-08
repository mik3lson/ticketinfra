from .client import NombaClient
#from django.conf import settings


class SubAccountClient:
    #BASE_URL = settings.NOMBA_BASE_URL

    ENDPOINT = "/accounts/sub-account"

    @classmethod
    def create(cls, account_name, account_ref):
        payload = {
            "accountName": account_name,
            "accountRef": account_ref,
        }

        return NombaClient.post(
            cls.ENDPOINT,
            json=payload,
        )
    
    @classmethod
    def list(cls):
        return NombaClient.get(
            cls.ENDPOINT,
        )
    
    @classmethod
    def get_balance(cls, sub_account_id):
        endpoint = f"{cls.ENDPOINT}/{sub_account_id}/balance"
        return NombaClient.get(
            endpoint,
        )