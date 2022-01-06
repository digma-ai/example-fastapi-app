from opentelemetry import trace

tracer = trace.get_tracer(__name__)

class DomainValidator:
    async def validate_user_exists(self, user_ids):
        
        with tracer.start_as_current_span("handled operation") as span:                    
            
            if len(user_ids)<4:
                raise AttributeError("under control")
               
            if len(user_ids)==4:
                raise Exception("can't find user")