from time import sleep
from typing import List, Optional
from fastapi.params import Query
import os

import sys
import traceback

import uvicorn as uvicorn
from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

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

digma_exporter = DigmaExporter()
user_service = UserService()

trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(digma_exporter, max_export_batch_size=10)
)
app = FastAPI()
FastAPIInstrumentor.instrument_app(app)
RequestsInstrumentor().instrument()
tracer = trace.get_tracer(__name__)
Instrumentator().instrument(app).expose(app)


def handle_exception(exc_type, exc_value, exc_traceback):
    print("here")


sys.excepthook = handle_exception


def trace_exceptions(frame, event, arg):
    if event != 'exception':
        return
    co = frame.f_code
    func_name = co.co_name
    line_no = frame.f_lineno
    filename = co.co_filename
    exc_type, exc_value, exc_traceback = arg
    print(exc_type)


def trace_calls(frame, event, arg):
    if event != 'call':
        return
    if event == 'exception':
        return

    co = frame.f_code

    func_name = co.co_name
    print(func_name)
    return trace_exceptions


@app.get("/users")
async def get_users():
    return {"message": "Hello World"}


@app.get("/validate/")
async def validate(user_ids: Optional[List[str]] = Query(None)):
    ids = str.split(user_ids[0], ',')

    with tracer.start_as_current_span("user validation"):
        try:
            await UserValidator().validate_user(ids)
        except:
            raise

    return "okay"


@app.get("/")
async def root():
    try:
        # raise_error()
        user_service.all()
    except Exception as ex:
        # ex_type, ex, tb = sys.exc_info()
        # ss = traceback.extract_tb(tb)
        raise Exception(f'error occurred : {str(ex)}')


@app.get("/flow1")
async def flow1():
    C().execute()


def error_print(someone):
    print('Hello, ' + someon)


@app.get("/flow2")
async def flow2():
    D().execute()


@app.get("/flow3")
async def flow3():
    error_print('asd')


@app.get("/flow4/{name}")
async def flow4(name: str):
    print(f'{name} {uknown_var}')


@app.get("/flow5")
async def flow5():
    print(f'bob {uknown_var}')


# def excepthook(type, value, tb):
#    traceback.print_exception(type, value, tb)

#    while tb.tb_next:
#        tb = tb.tb_next

#    print >>sys.stderr, 'Locals:',  tb.tb_frame.f_locals

#    print >>sys.stderr, 'Globals:', tb.tb_frame.f_globals

# sys.excepthook = excepthook
def throw_err():
    none_param = None
    foo = 1
    bar = 0
    foo / bar


@app.get("/flow6/{num}")
async def flow6(num: int):
    # print(100/num)
    try:
        local_var = 42
        print(eval("100/x", {"x": num}))
    except:
        ex_type, ex, tb = sys.exc_info()
        ss = traceback.extract_tb(tb)
        st = ss.format()
        raise


@app.get("/flow7")
async def flow7():
    throw_err()


@app.get("/flow8")  # handled error
async def flow8():
    try:
        with tracer.start_as_current_span("user validation"):
            throw_err()
    except:
        ...


@app.get("/flow9")  # unhandled error
async def flow9():
    with tracer.start_as_current_span("user validation"):
        throw_err()


@app.get("/flow10")  # unhandled error
async def flow10():
    with tracer.start_as_current_span("flow10") as s:
        span: Span = s
        span.set_attribute("att1", "value2")

    sleep(2)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
