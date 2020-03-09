from aiohttp import web

from settings import config
from views import routes
from db import init_mongo, close_mongo


app = web.Application()
app.router.add_routes(routes)

app['config'] = config

app.on_startup.append(init_mongo)
app.on_cleanup.append(close_mongo)

web.run_app(app)
