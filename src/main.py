from fastapi import FastAPI

from di_container import Container
from controllers import user_controller


def create_app() -> FastAPI:

    container = Container()
    container.config.from_yaml('config/config.yaml')
    container.config.from_yaml('config/config.yaml')
    app = FastAPI(
        title="auth-python",
        version="0.0.1",
    )
    container.wire(modules=[user_controller])
    app.container = container
    app.include_router(user_controller.router)

    return app


app = create_app()
