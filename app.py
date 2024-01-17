import os
import uvicorn
from fastapi import FastAPI
from omegaconf import OmegaConf

from src.containers.containers import AppContainer
from src.routes.routers import router as app_router
from src.routes import forest_routes


def create_app() -> FastAPI:
    cfg = OmegaConf.load('config/app_config.yaml')

    container = AppContainer()
    container.config.from_dict(cfg)
    container.wire([forest_routes])

    app = FastAPI()

    set_routers(app)

    return app


def set_routers(app: FastAPI):
    app.include_router(app_router, prefix='/forest_tags', tags=['forest_tags'])


if __name__ == '__main__':
    app = create_app()

    app_port = int(os.getenv('API_PORT'))
    app_host = os.getenv('HOST')

    uvicorn.run(app, port=app_port, host=app_host)
