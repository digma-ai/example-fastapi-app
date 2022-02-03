import requests
import uvicorn
from dotenv import load_dotenv
import git
import os

from fastapi import FastAPI
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from conf import PROJECT_ROOT
from conf.environment_variables import GIT_COMMIT_ID
from opentelemetry import trace
from opentelemetry.exporter.digma import DigmaExporter, register_batch_digma_exporter
from opentelemetry.propagate import set_global_textmap
from opentelemetry.propagators.b3 import B3Format

set_global_textmap(B3Format())
load_dotenv()

try:
    repo = git.Repo(search_parent_directories=True)

    os.environ[GIT_COMMIT_ID] = repo.head.object.hexsha
except:
    pass


resource = Resource(attributes={"service.name": "client_ms"})
trace.set_tracer_provider(TracerProvider(resource=resource))

"""
the following 3 lines are needed to register Digma exporter
"""
path = os.path.abspath(os.path.dirname(__file__))
os.environ.setdefault(PROJECT_ROOT, path)  # or set DIGMA_CONFIG_MODULE
register_batch_digma_exporter()



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
app = FastAPI()
FastAPIInstrumentor.instrument_app(app)
RequestsInstrumentor().instrument()
LoggingInstrumentor().instrument(set_logging_format=True)


tracer = trace.get_tracer(__name__)


@app.get("/")
async def root():
    print(f"in span {trace.get_current_span().get_span_context().span_id}")
    with tracer.start_as_current_span("admin console"):
        print(f"in span {trace.get_current_span().get_span_context().span_id}")
        response =  requests.get('http://localhost:8000/')
        response.raise_for_status()
        

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)