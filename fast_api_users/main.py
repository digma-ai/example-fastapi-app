import os
from typing import Optional

import git
import requests
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Header
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.sdk.resources import Resource, SERVICE_NAME
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from conf.environment_variables import GIT_COMMIT_ID, PROJECT_ROOT
from opentelemetry import trace
from opentelemetry.exporter.digma import register_batch_digma_exporter
from opentelemetry.instrumentation.digma import DigmaConfiguration
from test_instrumentation_helpers.test_instrumentation import OpenTelemetryTimeOverride, FastApiTestInstrumentation

load_dotenv()

try:
    repo = git.Repo(search_parent_directories=True)
    os.environ[GIT_COMMIT_ID] = repo.head.object.hexsha
except:
    pass

path = os.path.abspath(os.path.dirname(__file__))
os.environ.setdefault(PROJECT_ROOT, path)
digma_conf = DigmaConfiguration()\
    .trace_module('fastapi')\
    .trace_module('requests')

resource = Resource.create(attributes={SERVICE_NAME: 'users-ms'}).merge(digma_conf.resource)
provider = TracerProvider(resource=resource)
provider.add_span_processor(digma_conf.span_processor)
trace.set_tracer_provider(provider)

app = FastAPI()

FastAPIInstrumentor.instrument_app(app, server_request_hook=FastApiTestInstrumentation.server_request_hook)
RequestsInstrumentor().instrument()
LoggingInstrumentor().instrument(set_logging_format=True)
tracer = trace.get_tracer(__name__)


@app.get("/")
async def root(x_simulated_time: Optional[str] = Header(None)):
    headers = {}
    if x_simulated_time:
        headers['x-simulated-time'] = x_simulated_time
    print(f"in span {trace.get_current_span().get_span_context().span_id}")
    with tracer.start_as_current_span("user service console"):
        print(f"in span {trace.get_current_span().get_span_context().span_id}")
        response = requests.get('http://localhost:8001/', headers=headers)
        response.raise_for_status()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)
