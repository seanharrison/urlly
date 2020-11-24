from json.decoder import JSONDecodeError

from pydantic import ValidationError
from starlette.endpoints import HTTPEndpoint
from starlette.responses import JSONResponse

from app import tables
from app.types import URL, Result


class Home(HTTPEndpoint):
    def get(self, request):
        return JSONResponse(Result(message='Go on, then, shorten a URL.').dict())


class Urls(HTTPEndpoint):
    # async def get(self, request):
    #     records = await request.app.database.fetch_all(tables.urls.select())
    #     urls = [URL.construct(**record).dict() for record in records]
    #     result = Result(data={'urls': urls})
    #     return JSONResponse(result.dict())

    async def post(self, request):
        """
        POST a new URL to shorten. Request body:
        ```json
        {"target": "..."}
        ```
        Response:

        * If it doesn't look like a URL:
            ```json
            {"status": 422, "message": "Doesn't look like a URL to us, sorry."}
            ```
        * Otherwise, create it:
            ```json
            {"status": 201, "data": {"url": {"target": "...", "id": "..."}}}
            ```
        """
        try:
            data = await request.json()
            url = URL(**data)
            await request.app.database.execute(
                tables.urls.insert().values(**url.dict())
            )
            result = Result(data={'url': url.dict()}, status=201)
        except JSONDecodeError as exc:
            result = Result(message=str(exc), status=400)
        except ValidationError as exc:
            result = Result(errors=exc.errors(), status=422)

        return JSONResponse(result.dict(), status_code=result.status)


class Url(HTTPEndpoint):
    async def get(self, request):
        """
        GET the data for a URL with the given id

        * exists: {"status": 200, "data": {"url": {...}}}
        * not found: {"status": 404, "message": "Not Found"}
        """
        url_id = request.path_params['url_id']
        record = await request.app.database.fetch_one(
            tables.urls.select(tables.urls.c.id == url_id)
        )
        if not record:
            result = Result(status=404, message='Not Found')
        else:
            url = URL.construct(**record)
            result = Result(data={'url': url.dict()})

        return JSONResponse(result.dict(), status_code=result.status)
