from aiohttp import web

from settings import config
from views import routes

app = web.Application()
app.router.add_routes(routes)
app['config'] = config
web.run_app(app)
