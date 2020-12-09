from datetime import datetime

import orjson
from pydantic import BaseModel, validator

from app import lib, settings


class Type(BaseModel):
    def dict(self, exclude_none=True, **kwargs):
        """
        Override the built-in dict() method to exclude None by default.
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
    The base result object for our API.
    """

    status: int = 200
    message: str = None
    data: dict = None
    errors: list = None


class URL(Type):
    id: str = None  # the random id for this URL
    target: str  # the target location for this URL
    created: datetime = None  # when the URL was created

    @validator('id', pre=True, always=True)
    def id_gen_if_none(cls, value):
        if not value:
            value = lib.gen_id(settings.GEN_ID_BYTES)
        return value

    @validator('target')
    def target_is_url(cls, value):
        if not lib.is_url(value):
            raise ValueError("Doesn't look like a URL to us, sorry.")
        return value
