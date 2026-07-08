
from .nomba.subAccount import SubAccountClient
from base.models import Organizer

class OrganizerService:

    @classmethod
    def create_nomba_subaccount(cls, Organizer):
        account_ref = f"org_{Organizer.id}"

        response = SubAccountClient.create(
            account_name=Organizer.name,
            account_ref=account_ref,
        )

        data = response["data"]

        Organizer.nomba_subaccount_id = data["id"]
        Organizer.nomba_subaccount_ref = account_ref

        Organizer.save(
            update_fields=[
                "nomba_subaccount_id",
                "nomba_subaccount_ref",
            ]
        )

        return Organizer