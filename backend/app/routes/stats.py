from fastapi import APIRouter, Depends

from app.schemas import StatsResponse
from app.services import DefaultStatsService, StatsService

router = APIRouter(prefix="/api/stats", tags=["Statistics"])


def get_stats_service() -> StatsService:
    raise NotImplementedError("Override via dependencies")


@router.get("", response_model=StatsResponse)
async def get_stats(service: StatsService = Depends(get_stats_service)):
    return await service.get_stats()
