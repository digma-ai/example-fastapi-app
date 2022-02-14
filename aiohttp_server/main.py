import os
from aiohttp import web

from digma_instrumentation.configuration import Configuration
from digma_instrumentation.opentelemetry_utils import opentelemetry_init, opentelemetry_aiohttp_middleware


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
conf = Configuration().trace_this_package()
opentelemetry_init(service_name='providers',
                   digma_conf=conf,
                   digma_endpoint="http://34.254.64.15:5050")

app = web.Application(middlewares=[error_middleware, opentelemetry_aiohttp_middleware(__name__)])
app.add_routes([web.get('/', root),
                web.get('/validate', validate)])

if __name__ == '__main__':
    web.run_app(app, port=8004)
