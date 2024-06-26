from fastapi import FastAPI

from app.api import router as api_router


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(router=api_router)

    return app
