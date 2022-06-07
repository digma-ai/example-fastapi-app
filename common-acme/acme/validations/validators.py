import random

from opentelemetry import trace
import asyncio
tracer = trace.get_tracer(__name__)

def validate_user(username: str):
    if not username:
        raise InvalidInput('Empty username value')

    validate_authorization(username)


def validate_authorization(username: str):
    if username != 'admin':
        raise AuthorizationError()

async def sleep(t): 
    with tracer.start_as_current_span("sleep-span"):
        await asyncio.sleep(t+random.random()-0.5)  # t-0.5 <-> t+0.5  sec

class InvalidInput(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class AuthorizationError(Exception):
    pass
