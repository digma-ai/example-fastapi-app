import os
from aiohttp import web
from digma.instrumentation.test_tools import digma_opentelemetry_bootstrap_for_testing
from opentelemetry.instrumentation.digma import DigmaConfiguration
from opentelemetry.instrumentation.digma.opentelemetry_utils import opentelemetry_aiohttp_middleware


@web.middleware
async def error_middleware(request, handler):
    try:
        return await handler(request)
    except Exception as e:
        return web.json_response(text='Internal Server Error: '+str(e), status=500)


async def root(request: web.Request):
    name = request.rel_url.query.get('name', "Anonymous")
    if name == 'asaf':
        raise Exception('Bad name error!!!')
    return web.Response(text='All good')


async def validate(request: web.Request):
    raise Exception('Bad validation error!!!')

os.environ['ENVIRONMENT'] = 'dryrun'
digma_opentelemetry_bootstrap_for_testing(service_name='aiohttp-ms',
                                          configuration=DigmaConfiguration()
                                          .trace_this_package(),
                                          digma_backend="http://localhost:5050")


app = web.Application(middlewares=[error_middleware, opentelemetry_aiohttp_middleware(__name__)])
app.add_routes([web.get('/', root),
                web.get('/validate', validate)])

if __name__ == '__main__':
    web.run_app(app, port=8004)
