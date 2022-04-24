import asyncio

import requests
from starlette.concurrency import run_in_threadpool

from opentelemetry import trace

tracer = trace.get_tracer(__name__)


class DomainValidator:
    async def validate_user_exists(self, user_ids):

        with tracer.start_as_current_span("validating users") as span:

            if len(user_ids) == 2:
                return

            if len(user_ids) > 4:
                rst = await run_in_threadpool(lambda: requests.get('http://localhost:8001/validate'))
                return rst

            if len(user_ids) < 4:
                raise AttributeError("under control")

            if len(user_ids) == 4:
                raise Exception(f"can't find user {user_ids[0]}")

    async def validate_permissions(self):

        with tracer.start_as_current_span("check_db_permission") as span:
            test = __name__
            print(test)
            permitted = await PermissionsDb.CheckCurrentPer(Permisson.current_context)
            return permitted;


    async def validate_group_exists(self, user_ids):

        with tracer.start_as_current_span("validating groups") as span:

            if len(user_ids) > 4 or len(user_ids)==1:
                rst = await run_in_threadpool(lambda: requests.get('http://digma.ai:5555'))
                return rst

            if len(user_ids) < 4:
                raise AttributeError("under control")

            if len(user_ids) == 4:
                raise Exception(f"can't find user {user_ids[0]}")




class PermissionsDb:
    @staticmethod
    async def CheckCurrentPer(arg):
        await asyncio.sleep(4)
        return True

class Permisson:
    @staticmethod
    def current_context():
        return "2"