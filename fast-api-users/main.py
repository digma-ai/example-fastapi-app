from typing import Optional

import requests
import uvicorn
from dotenv import load_dotenv
import git
import os

from fastapi import FastAPI, Header
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry import trace
from opentelemetry.exporter.digma import DigmaExporter
from opentelemetry.propagate import set_global_textmap
from opentelemetry.propagators.b3 import B3Format

from test_instrumentation import OpenTelemetryTimeOverride, FastApiTestInstrumentation

set_global_textmap(B3Format())
load_dotenv()

repo = git.Repo(search_parent_directories=True)
os.environ['GIT_COMMIT_ID'] = repo.head.object.hexsha
path = os.path.abspath(os.path.dirname(__file__))
os.environ.setdefault("PROJECT_ROOT", path )
os.environ.setdefault("DIGMA_CONFIG_MODULE", "digma_config")  # must be set by customer

resource = Resource(attributes={"service.name": "user_ms"})
trace.set_tracer_provider(TracerProvider(resource=resource))
digma_exporter = DigmaExporter(pre_processors=[OpenTelemetryTimeOverride.test_overrides])

trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(digma_exporter, max_export_batch_size=10)
)

otel_trace = os.environ.get("OTELE_TRACE", None)
if otel_trace == 'True':
    from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import (
        OTLPSpanExporter,
    )

    otlp_exporter = OTLPSpanExporter(endpoint="http://localhost:4317", insecure=True)
    trace.get_tracer_provider().add_span_processor(
        BatchSpanProcessor(otlp_exporter)
    )
app = FastAPI()
FastAPIInstrumentor.instrument_app(app, server_request_hook=FastApiTestInstrumentation.server_request_hook)
RequestsInstrumentor().instrument()
LoggingInstrumentor().instrument(set_logging_format=True)


tracer = trace.get_tracer(__name__)


@app.get("/")
async def root(x_simulated_time: Optional[str] = Header(None)):
    headers ={}
    if x_simulated_time:
        headers['x-simulated-time']=x_simulated_time
    print(f"in span {trace.get_current_span().get_span_context().span_id}")
    with tracer.start_as_current_span("user service console"):
        print(f"in span {trace.get_current_span().get_span_context().span_id}")
        response =  requests.get('http://localhost:8001/', headers=headers)
        response.raise_for_status()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)