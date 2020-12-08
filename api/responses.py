import orjson
from starlette.responses import JSONResponse


class ORJSONResponse(JSONResponse):
    def render(self, content):
        return orjson.dumps(content)
