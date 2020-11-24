import pytest
from starlette.testclient import TestClient

from app.main import app


@pytest.fixture(scope="session")
def client():
    with TestClient(app) as testclient:
        yield testclient
