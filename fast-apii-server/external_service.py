import requests
class ExternalValidation:

    async def validate_with_external_service(self, users_ids):
        if len(users_ids)>4:
            requests.get('https://digma.ai:7055')
        else:
            return True