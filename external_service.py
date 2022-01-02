import requests
class ExternalValidation:
    def validate_with_external_service(self, users_ids):
        if len(users_ids)>4:
            raise ConnectionError("blah")
        else:
            return True