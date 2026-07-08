from .client import NombaClient


def create_virtual_account(payload):
    return NombaClient.request(
        "POST",
        "/virtual-account",
        json=payload,
    )