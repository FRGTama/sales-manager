from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import init_db
from app.routes import agencies as agencies_router
from app.routes import sales as sales_router
from app.routes import stats as stats_router
from app.routes import track_records as track_records_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    await init_db()
    yield


def create_app() -> FastAPI:
    app = FastAPI(title="Sharework Sales Management API", lifespan=lifespan)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(sales_router.router)
    app.include_router(agencies_router.router)
    app.include_router(track_records_router.router)
    app.include_router(stats_router.router)

    return app


app = create_app()
