from datetime import datetime

import orjson
from pydantic import BaseModel, validator

from app import lib, settings


class Type(BaseModel):
    def dict(self, exclude_none=True, **kwargs):
        """
        Override the pydantic BaseModel.dict() method to exclude None by default.
        """
        return super().dict(exclude_none=exclude_none, **kwargs)

    def json(self, exclude_none=True, **kwargs):
        """
        Use orjson to serialize model date more quickly. Exclude None by default.
        """
        return orjson.dumps(
            self.dict(exclude_none=exclude_none, **kwargs),
        )


class Result(Type):
    """
    The base result object for our API: All API responses return one of these.

    * status (int) = HTTP status code, default 200
    * message (str) = Result message
    * data (dict) = Result data
    * errors (list) = Validation or other errors
    """
    status: int = 200
    message: str = None
    data: dict = None
    errors: list = None


class URL(Type):
    """
    URL instance data, matching the database schema:

    * id (str) = the random id for this URL, which is also its "short code"
    * target (str) = the target location for this URL instance -- the target URL itself
    * created (datetime) = timestamp when the URL was created
    """
    id: str = None
    target: str
    created: datetime = None

    @validator('id', pre=True, always=True)
    def id_gen_if_none(cls, value):
        """
        Automatically generate an id if there's none.
        """
        if not value:
            value = lib.gen_id(settings.GEN_ID_BYTES)
        return value

    @validator('target')
    def target_is_url(cls, value):
        """
        Ensure that the target is a URL (via `app.lib.is_url`).
        """
        if not lib.is_url(value):
            raise ValueError("Doesn't look like a URL to us, sorry.")
        return value
