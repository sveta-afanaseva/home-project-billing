import uvicorn
from fastapi import FastAPI

from app.api.routers import account
from app.sql_app.database import init_models


def create_app() -> FastAPI:
    app = FastAPI(docs_url="/", redoc_url=None)

    @app.on_event("startup")
    async def startup():
        await init_models()

    app.include_router(account.router)
    return app


if __name__ == "__main__":
    uvicorn.run(create_app())
