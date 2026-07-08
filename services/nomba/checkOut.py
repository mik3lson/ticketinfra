from .client import NombaClient


def create_checkout(payload):
    return NombaClient.request(
        "POST",
        "/checkout",
        json=payload,
    )