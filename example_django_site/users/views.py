import asyncio
from django.shortcuts import render

from django.http import HttpResponse
from opentelemetry import trace

tracer = trace.get_tracer(__name__)

async def index(request):
    with tracer.start_as_current_span("get users"):
        await asyncio.sleep(2)

    with tracer.start_as_current_span("create index result"):
        await asyncio.sleep(0.2)

    return HttpResponse("Done")


async def list(request):
    with tracer.start_as_current_span("getting user list "):
        await asyncio.sleep(0.2)

    with tracer.start_as_current_span("create list result"):
        await asyncio.sleep(0.2)

    return HttpResponse("Done")
