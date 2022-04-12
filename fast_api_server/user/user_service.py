from fast_api_server.user.user_store import UserStore
from fast_api_server.user_validation import UserValidator
from opentelemetry import trace

tracer = trace.get_tracer(__name__)


class UserException(Exception):
    pass


class UserService:
    def __init__(self):
        self.user_store = UserStore()
        self.validator = UserValidator()

    def all(self, id):
        with tracer.start_as_current_span("retrieve users"):
            if (id == '1'):
                raise Exception("blah")
            users = self.user_store.get_users()
            self.printusers(users)

    def print_users(self, users):
        for user in users:
            print(user.name)

    async def validate(self, user_name):

        with tracer.start_as_current_span("validate users") as span:
            try:
                await self.user_store.get_user(user_name)
            except UserException as e:
                span.record_exception(e)
                raise e

            self.validator.validate_user(user_name)


    def process(self, users):
        self.print_users(users)
