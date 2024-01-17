import os
import pytest
from omegaconf import OmegaConf

from fastapi import FastAPI
from fastapi.testclient import TestClient

from app import set_routers
from src.containers.containers import AppContainer
from src.routes import forest_routes


@pytest.fixture(scope='session')
def test_image():
    f = open(os.path.join('tests', 'images', 'test.jpg'), 'rb')  # noqa: WPS515
    try:
        yield f.read()
    finally:
        f.close()


@pytest.fixture(scope='session')
def app_config():
    return OmegaConf.load(os.path.join('tests', 'test_config.yaml'))


@pytest.fixture
def wired_app_container(app_config):
    container = AppContainer()
    container.config.from_dict(app_config)
    container.wire([forest_routes])
    yield container
    container.unwire()


@pytest.fixture
def test_app(wired_app_container):
    app = FastAPI()
    set_routers(app)
    return app


@pytest.fixture
def client(test_app):
    return TestClient(test_app)
