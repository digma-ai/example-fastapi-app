from database_validation import DomainValidator
from external_service import ExternalValidation
from opentelemetry import trace

tracer = trace.get_tracer(__name__)

class UserValidator:

    async def validate_user(self, user_ids):

        if (ExternalValidation().validate_with_external_service(user_ids)):
            with tracer.start_as_current_span("db validation") as span:                    
                await DomainValidator().validate_user_exists(user_ids)
        else:
            raise Exception("validation error")