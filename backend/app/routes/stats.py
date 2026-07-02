from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.repositories import StatsRepository
from app.schemas import StatsResponse
from app.services import StatsService

router = APIRouter(prefix="/api/stats", tags=["Statistics"])


async def get_stats_service(db: AsyncSession = Depends(get_db)) -> StatsService:
    return StatsService(StatsRepository(db))


@router.get("", response_model=StatsResponse)
async def get_stats(service: StatsService = Depends(get_stats_service)):
    return await service.get_stats()
