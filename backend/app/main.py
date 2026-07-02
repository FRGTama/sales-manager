from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db, init_db
from app.repositories import (
    SQLAgencyRepository,
    SQLSaleRepository,
    SQLStatsRepository,
    SQLTrackRecordRepository,
)
from app.routes import agencies as agencies_router
from app.routes import sales as sales_router
from app.routes import stats as stats_router
from app.routes import track_records as track_records_router
from app.services import (
    DefaultAgencyService,
    DefaultSaleService,
    DefaultStatsService,
    DefaultTrackRecordService,
)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    await init_db()
    yield


async def get_sale_service(db: AsyncSession = Depends(get_db)) -> DefaultSaleService:
    sale_repo = SQLSaleRepository(db)
    agency_repo = SQLAgencyRepository(db)
    return DefaultSaleService(sale_repo, agency_repo)


async def get_agency_service(db: AsyncSession = Depends(get_db)) -> DefaultAgencyService:
    agency_repo = SQLAgencyRepository(db)
    sale_repo = SQLSaleRepository(db)
    return DefaultAgencyService(agency_repo, sale_repo)


async def get_track_record_service(db: AsyncSession = Depends(get_db)) -> DefaultTrackRecordService:
    record_repo = SQLTrackRecordRepository(db)
    agency_repo = SQLAgencyRepository(db)
    return DefaultTrackRecordService(record_repo, agency_repo)


async def get_stats_service(db: AsyncSession = Depends(get_db)) -> DefaultStatsService:
    stats_repo = SQLStatsRepository(db)
    return DefaultStatsService(stats_repo)


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

    app.dependency_overrides[sales_router.get_sale_service] = get_sale_service
    app.dependency_overrides[agencies_router.get_agency_service] = get_agency_service
    app.dependency_overrides[track_records_router.get_track_record_service] = get_track_record_service
    app.dependency_overrides[stats_router.get_stats_service] = get_stats_service

    return app


app = create_app()
