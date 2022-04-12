import asyncio
from opentelemetry import trace

tracer = trace.get_tracer(__name__)



class UserStore:
    def get_users(self):
        return None

    async def get_user(self, username):
        with tracer.start_as_current_span("get from db") as span:
            await asyncio.sleep(2)
            return username


class InMemoryUserStore1(UserStore):
    def get_users(self):
        raise ValueError('invalid value')


class InMemoryUserStore2(UserStore):
    def get_users(self):
        raise ValueError('invalid value')
