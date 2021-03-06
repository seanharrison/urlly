from databases import Database
from starlette.applications import Starlette
from starlette.routing import Route

from app import settings

from . import endpoints

database = Database(settings.DATABASE_URL, force_rollback=settings.TESTING)

routes = [
    Route('/', endpoints.Home),
    Route('/urls', endpoints.Urls),
    Route('/urls/{url_id}', endpoints.Url),
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
