import os

import sys
import traceback

import uvicorn as uvicorn
from fastapi import FastAPI

from flows import D, C, A
from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
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


@app.get("/users")
async def get_users():
    raise Exception("test exception")
    return {"message": "Hello World"}


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

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
