from typing import List, Optional
from fastapi.params import Query
import os

import sys
import traceback
import uvicorn as uvicorn
from fastapi import FastAPI
from opentelemetry.instrumentation.logging import LoggingInstrumentor

from flows import D, C, A
from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider, Span
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.digma import DigmaExporter

from user.user_service import UserService
import git
from dotenv import load_dotenv



class ClassA:
    def exec(self, func):
        func()


class ClassB:
    def exec(self, func):
        func()

load_dotenv()

repo = git.Repo(search_parent_directories=True)
os.environ['GIT_COMMIT_ID'] = repo.head.object.hexsha

from opentelemetry.instrumentation.requests import RequestsInstrumentor
from user_validation import UserValidator

# You can optionally pass a custom TracerProvider to instrument().

resource = Resource(attributes={"service.name": "fastapi-blog"})
trace.set_tracer_provider(TracerProvider(resource=resource))
tracer = trace.get_tracer(__name__)

os.environ.setdefault("DIGMA_CONFIG_MODULE", "digma_config")  # must be set by customer
digma_exporter = DigmaExporter()
user_service = UserService()

trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(digma_exporter, max_export_batch_size=10)
)
app = FastAPI()
FastAPIInstrumentor.instrument_app(app)
RequestsInstrumentor().instrument()
tracer = trace.get_tracer(__name__)
LoggingInstrumentor().instrument(set_logging_format=True)




def handle_exception(exc_type, exc_value, exc_traceback):
    print("here")


sys.excepthook = handle_exception


@app.get("/users")
async def get_users():
    return {"message": "Hello World"}


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
        #raise_error()
        user_service.all()
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


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
    