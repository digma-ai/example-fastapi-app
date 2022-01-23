import os
from typing import List, Optional

import git
import uvicorn as uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.params import Query
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.propagators.b3 import B3Format
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider, Span
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from opentelemetry.exporter.digma import DigmaExporter
from opentelemetry.propagate import set_global_textmap

from flows import D, C, recursive_call
from opentelemetry import trace
from user.user_service import UserService
from user_validation import UserValidator

set_global_textmap(B3Format())
load_dotenv()

repo = git.Repo(search_parent_directories=True)
os.environ['GIT_COMMIT_ID'] = repo.head.object.hexsha
path = os.path.abspath(os.path.dirname(__file__) + os.path.sep + os.path.pardir)
os.environ.setdefault("PROJECT_ROOT", path )
os.environ.setdefault("DIGMA_CONFIG_MODULE", "digma_config")  # must be set by customer


resource = Resource(attributes={"service.name": "fastapi-blog"})
trace.set_tracer_provider(TracerProvider(resource=resource))
tracer = trace.get_tracer(__name__)

# when project root is not part of the PythonPath.
# PythonPath should be the path to your project
# sys.path.append(dirname(dirname(abspath(__file__))))
os.environ.setdefault("DIGMA_CONFIG_MODULE", "digma_config")  # must be set by customer
digma_exporter = DigmaExporter()
user_service = UserService()

trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(DigmaExporter(), max_export_batch_size=10))

otel_trace = os.environ.get("OTELE_TRACE", None)
if otel_trace == 'True':
    from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import (
        OTLPSpanExporter,
    )

    otlp_exporter = OTLPSpanExporter(endpoint="http://localhost:4317", insecure=True)
    trace.get_tracer_provider().add_span_processor(
        BatchSpanProcessor(otlp_exporter)
    )


LoggingInstrumentor().instrument(set_logging_format=True)

app = FastAPI()
FastAPIInstrumentor.instrument_app(app)
RequestsInstrumentor().instrument()
tracer = trace.get_tracer(__name__)

user_service = UserService()


@app.get("/users1")
async def get_users():
    with tracer.start_as_current_span("user validation"):
        try:
            await UserValidator().validate_user(["2","2","3","4"])
        except:
            raise Exception("here")

@app.get("/users")
async def get_users():
    with tracer.start_as_current_span("user validation"):
        user_service.some(None)

@app.get("/validate/")
async def validate(user_ids: Optional[List[str]] = Query(None)):
    ids = str.split(user_ids[0],',')
    
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


@app.get("/flow1")
async def flow1():
   C().execute()

@app.get("/flow2")
async def flow2():
   D().execute()

@app.get("/flow4")
async def flow4():
    print(uknown_var)


@app.get("/flow5/{num}")
async def flow5(num: int):
    # try:
    local_var = 42

    print(eval("100/x", {"x": num}))
    # except:
    #     ex_type, ex, tb = sys.exc_info()
    #     ss = traceback.extract_tb(tb)
    #     st = ss.format()
    #     raise
@app.get("/flow6")  # unhandled error
async def flow6():
    with tracer.start_as_current_span("flow6") as s:
        span: Span = s
        span.set_attribute("att1", "value2")

        print(uknown_var)

@app.get("/flow7")  # unhandled error
async def flow7():
    user_service.all()

@app.get("/flow8")  # unhandled error
async def flow8():
    recursive_call()

@app.get("/flow9")  # unhandled error
async def flow9():
    recursive_call()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
    