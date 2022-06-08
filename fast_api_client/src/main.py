import os
from typing import Optional

import aio_pika
import git
import requests
import uvicorn
from acme.validations import validators
from aio_pika import connect
from digma.instrumentation.test_tools import digma_opentelemetry_bootstrap_for_testing
from digma.instrumentation.test_tools.helpers import FastApiTestInstrumentation
from dotenv import load_dotenv
from fastapi import FastAPI, Header, Query
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from starlette import status

from opentelemetry import trace
from opentelemetry.instrumentation.digma import DigmaConfiguration


load_dotenv()

try:
    repo = git.Repo(search_parent_directories=True)
    os.environ['GIT_COMMIT_ID'] = repo.head.object.hexsha
except:
    pass

digma_opentelemetry_bootstrap_for_testing(service_name='client-ms',
                                          configuration=DigmaConfiguration().trace_this_package(root='../')
                                          .trace_package('acme'),
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
    with tracer.start_as_current_span("admin console"):
        print(f"in span {trace.get_current_span().get_span_context().span_id}")
        response = requests.get('http://localhost:8000/login', headers=headers)
        response.raise_for_status()


@app.get("/login")
async def validate(x_simulated_time: Optional[str] = Header(None)):
    headers = {}
    if x_simulated_time:
        headers['x-simulated-time'] = x_simulated_time
    print(f"in span {trace.get_current_span().get_span_context().span_id}")
    with tracer.start_as_current_span("admin console"):
        print(f"in span {trace.get_current_span().get_span_context().span_id}")
        response = requests.get('http://localhost:8000/login', headers=headers)
        response.raise_for_status()


@app.get("/validate")
async def validate(username=Query(None)):
    validators.validate_user(username)
    return True

@app.get("/process")
async def process():
    connection = await connect("amqp://admin:guest@localhost/")

    channel: aio_pika.abc.AbstractChannel = await connection.channel()

    queue = await channel.declare_queue("TransationProcessing")

    await channel.default_exchange.publish(
        aio_pika.Message(
            body='Hello {}'.format(queue.name).encode()
        ),
        routing_key=queue.name
    )

    await connection.close()

    return status.HTTP_200_OK


@app.get("/check/{delay}")
async def check(delay: str):
    await validators.sleep(int(delay))
    return status.HTTP_200_OK

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
