from pathlib import Path

from databases import Database
from starlette.applications import Starlette
from starlette.routing import Mount, Route
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

import api.main
from app import endpoints, settings

database = Database(settings.DATABASE_URL, **settings.DATABASE_PARAMS)

routes = [
    Route('/', endpoints.Home, name='home'),
    Mount('/api', routes=api.main.routes),
    Route('/{url_id}', endpoints.Url, name='url'),
]


async def on_startup():
    app.database = database
    await app.database.connect()


async def on_shutdown():
    await app.database.disconnect()


app = Starlette(
    routes=routes,
    debug=settings.DEBUG,
    on_startup=[on_startup],
    on_shutdown=[on_shutdown],
)

app.settings = settings
app.templates = Jinja2Templates(directory=Path(__file__).parent / 'templates')
