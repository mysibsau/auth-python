from fastapi import FastAPI

from di_container import Container
from routers import user_router


def create_app() -> FastAPI:

    container = Container()
    app = FastAPI(
        title="auth-python",
        version="0.0.1",
    )
    container.wire(modules=[user_router])
    app.container = container
    app.include_router(user_router.router)

    return app


app = create_app()
