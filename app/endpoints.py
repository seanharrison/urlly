from starlette.endpoints import HTTPEndpoint
from starlette.responses import RedirectResponse, Response

from app import tables


class Home(HTTPEndpoint):
    async def get(self, request):
        return request.app.templates.TemplateResponse(
            'index.html', {'request': request}
        )


class Url(HTTPEndpoint):
    async def get(self, request):
        """
        Look up the URL associated with the url_id in the path, and redirect to it, or
        return 404 Not Found if it doesn't exist.
        """
        url_id = request.path_params['url_id']
        record = await request.app.database.fetch_one(
            tables.urls.select(tables.urls.c.id == url_id)
        )
        if not record:
            return Response('Not Found', status_code=404)
        else:
            url = record['target']
            await request.app.database.execute(
                tables.urls_log.insert(), values={'url_id': record['id']}
            )
            return RedirectResponse(url=url, status_code=301)
