from database_validation import DomainValidator
from external_service import ExternalValidation


class UserValidator:

    def validate_user(self, user_ids):
        
        if (ExternalValidation().validate_with_external_service(user_ids)):
            DomainValidator().validate_user_exists(user_ids)
        else:
            raise Exception("validation error")