import os
from typing import Optional

import git
import requests
import uvicorn
from digma.instrumentation.test_tools import digma_opentelemetry_bootstrap_for_testing
from digma.instrumentation.test_tools.helpers import FastApiTestInstrumentation
from dotenv import load_dotenv
from fastapi import FastAPI, Header
from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor

from opentelemetry.instrumentation.digma import DigmaConfiguration

load_dotenv()

try:
    repo = git.Repo(search_parent_directories=True)
    os.environ['GIT_COMMIT_ID'] = repo.head.object.hexsha
except:
    pass


digma_opentelemetry_bootstrap_for_testing(service_name='users-ms',
                                          configuration=DigmaConfiguration().trace_this_package(root='../').trace_package('acme'),
                                          digma_backend="http://localhost:5050")


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
