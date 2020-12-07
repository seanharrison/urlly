from databases import Database
from starlette.applications import Starlette
from starlette.routing import Mount, Route

import api.main
from app import endpoints, settings

database = Database(settings.DATABASE_URL, force_rollback=settings.TESTING)

routes = [
    Mount('/api', routes=api.main.routes),
    Route('/{url_id}', endpoints.Url),
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
