import os
import random
from typing import List, Optional

import git
import uvicorn as uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.params import Query
from database_validation import Permisson

from database_validation import DomainValidator
from opentelemetry.instrumentation.digma import DigmaConfiguration
from root_api_response import RootApiResponse
from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor


from user.user_service import UserService
from user_validation import UserValidator
from flows import recursive_call
from digma.instrumentation.test_tools import digma_opentelemetry_bootstrap_for_testing
from digma.instrumentation.test_tools.helpers import FastApiTestInstrumentation

load_dotenv()

try:
    repo = git.Repo(search_parent_directories=True)
    os.environ['GIT_COMMIT_ID'] = repo.head.object.hexsha
except:
    pass

lam =  lambda conf: print("hello")

digma_opentelemetry_bootstrap_for_testing(service_name='server-ms', digma_backend="http://localhost:5050",
                                          configuration=DigmaConfiguration().trace_this_package()
                                          .set_environment('dev'))

# digma_conf = Configuration()\
#     .trace_this_package()

# resource = Resource.create(attributes={SERVICE_NAME: 'server-ms'}).merge(digma_conf.resource)
# provider = TracerProvider(resource=resource)
# provider.add_span_processor(digma_conf.span_processor)
# trace.set_tracer_provider(provider)

app = FastAPI()
FastAPIInstrumentor.instrument_app(app, server_request_hook=FastApiTestInstrumentation.server_request_hook,
                                   client_request_hook=FastApiTestInstrumentation.client_request_hook,
                                   client_response_hook=FastApiTestInstrumentation.client_response_hook)
RequestsInstrumentor().instrument()
LoggingInstrumentor().instrument(set_logging_format=True)
tracer = trace.get_tracer(__name__)

user_service = UserService()


# @app.get("/users1")
# async def get_users():
#     with tracer.start_as_current_span("user validation"):
#         try:
#             await UserValidator().validate_user(["2", "2", "3", "4"])
#         except:
#             raise Exception("here")


@app.get("/users")
async def get_users():
    with tracer.start_as_current_span("user validation"):
        user_service.some(None)


@app.get("/")
async def root():
    try:
        with tracer.start_as_current_span("root"):

            await DomainValidator().validate_permissions()

            return RootApiResponse().render()

    except Exception as ex:
        # ex_type, ex, tb = sys.exc_info()
        # ss = traceback.extract_tb(tb)
        raise Exception(f'error occurred : {str(ex)}')


@app.get("/validate/")
async def validate(user_ids: Optional[List[str]] = Query(None)):
    ids = str.split(user_ids[0], ',')

    await DomainValidator().validate_permissions()

    await DomainValidator().validate_group_exists(["admins"])


    with tracer.start_as_current_span("user validation"):
        await UserValidator().validate_user(ids)

    return "okay"


@app.get("/process")
async def process():
    with tracer.start_as_current_span("user validation"):
        await DomainValidator().validate_permissions()


@app.get("/login")
async def login():
    try:
        with tracer.start_as_current_span("login validation"):
            await user_service.validate(Permisson.current_context)
    except Exception as ex:
        # ex_type, ex, tb = sys.exc_info()
        # ss = traceback.extract_tb(tb)
        raise Exception(f'error occurred : {str(ex)}')

@app.get("/validateuser")
async def validate_user():
    try:
        await user_service.validate("2")
    except Exception as ex:
        # ex_type, ex, tb = sys.exc_info()
        # ss = traceback.extract_tb(tb)
        raise Exception(f'error occurred : {str(ex)}')


@app.get("/uservalidation")  # unhandled error
async def user_validation():
    user_service.validate()


@app.get("/flow8")  # unhandled error
async def flow8():
    recursive_call()


@app.get("/exception_generator")
async def chaos():
    raise type(f'Exception{random.randint(0, 100000)}', (Exception,), {})


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
