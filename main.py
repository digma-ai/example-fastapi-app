from typing import List, Optional
from fastapi.params import Query
import uvicorn as uvicorn
from fastapi import FastAPI
from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.digma import DigmaExporter
from user_service import UserService
from user_store import UserStore

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


@app.get("/users")
async def get_users():
    raise Exception("test exception")
    return {"message": "Hello World"}


@app.get("/validate/")
async def validate(user_ids: Optional[List[str]] = Query(None)):
    ids = str.split(user_ids[0],',')
    UserValidator().validate_user(ids)
    return "okay"


@app.get("/")
async def root():
    user_service.all()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
    