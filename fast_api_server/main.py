import os
from typing import List, Optional

import git
import uvicorn as uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.params import Query
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.propagate import set_global_textmap
from opentelemetry.propagators.b3 import B3Format
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider

from conf import DIGMA_CONFIG_MODULE
from conf.environment_variables import GIT_COMMIT_ID
from flows import recursive_call
from opentelemetry import trace
from opentelemetry.exporter.digma import register_batch_digma_exporter
from test_instrumentation_helpers.test_instrumentation import OpenTelemetryTimeOverride, FastApiTestInstrumentation
from user.user_service import UserService
from user_validation import UserValidator

set_global_textmap(B3Format())  # todo shay @roni why we need it??
load_dotenv()

try:
    repo = git.Repo(search_parent_directories=True)

    os.environ[GIT_COMMIT_ID] = repo.head.object.hexsha
except:
    pass

resource = Resource(attributes={"service.name": "fastapi-blog"})
trace.set_tracer_provider(TracerProvider(resource=resource))
tracer = trace.get_tracer(__name__)


"""
the following 2 lines are needed to register Digma exporter
"""
os.environ.setdefault(DIGMA_CONFIG_MODULE, "digma_config")  # or set PROJECT_ROOT
register_batch_digma_exporter(pre_processors=[OpenTelemetryTimeOverride.test_overrides])

# otel_trace = os.environ.get("OTELE_TRACE", None)
# if otel_trace == 'True':
#     from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import (
#         OTLPSpanExporter,
#     )
#
#     otlp_exporter = OTLPSpanExporter(endpoint="http://localhost:4317", insecure=True)
#     trace.get_tracer_provider().add_span_processor(
#         BatchSpanProcessor(otlp_exporter)
#     )

# LoggingInstrumentor().instrument(set_logging_format=True)

app = FastAPI()

FastAPIInstrumentor.instrument_app(app, server_request_hook=FastApiTestInstrumentation.server_request_hook,
                                   client_request_hook=FastApiTestInstrumentation.client_request_hook,
                                   client_response_hook=FastApiTestInstrumentation.client_response_hook)

user_service = UserService()


@app.get("/users1")
async def get_users():
    with tracer.start_as_current_span("user validation"):
        try:
            await UserValidator().validate_user(["2", "2", "3", "4"])
        except:
            raise Exception("here")


@app.get("/users")
async def get_users():
    with tracer.start_as_current_span("user validation"):
        user_service.some(None)


@app.get("/validate/")
async def validate(user_ids: Optional[List[str]] = Query(None)):
    ids = str.split(user_ids[0], ',')

    with tracer.start_as_current_span("user validation"):
        try:
            await UserValidator().validate_user(ids)
        except:
            raise Exception(f"wow exception on {user_ids[0]}")

    return "okay"


@app.get("/")
async def root():
    try:
        user_service.all("1")
    except Exception as ex:
        # ex_type, ex, tb = sys.exc_info()
        # ss = traceback.extract_tb(tb)
        raise Exception(f'error occurred : {str(ex)}')


@app.get("/validate/")
async def validate(user_ids: Optional[List[str]] = Query(None)):
    ids = str.split(user_ids[0], ',')

    with tracer.start_as_current_span("user validation"):
        try:
            await UserValidator().validate_user(ids)
        except:
            raise Exception(f"wow exception on {user_ids[0]}")

    return "okay"


@app.get("/validateuser")
async def validate_user():
    try:
        user_service.all("2")
    except Exception as ex:
        # ex_type, ex, tb = sys.exc_info()
        # ss = traceback.extract_tb(tb)
        raise Exception(f'error occurred : {str(ex)}')


@app.get("/flow7")  # unhandled error
async def flow7():
    user_service.all()


@app.get("/flow8")  # unhandled error
async def flow8():
    recursive_call()


@app.get("/flow10")
async def flow10():
    test_value = None
    test_value_none = None
    recursive_call()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)