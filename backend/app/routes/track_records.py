from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.repositories import TrackRecordRepository, AgencyRepository
from app.schemas import TrackRecordCreate, TrackRecordResponse, TrackRecordUpdate
from app.services import TrackRecordService

router = APIRouter(prefix="/api/track-records", tags=["Track Records"])


async def get_track_record_service(db: AsyncSession = Depends(get_db)) -> TrackRecordService:
    return TrackRecordService(TrackRecordRepository(db), AgencyRepository(db))


@router.get("", response_model=list[TrackRecordResponse])
async def list_track_records(service: TrackRecordService = Depends(get_track_record_service)):
    return await service.list_track_records()


@router.post("", response_model=TrackRecordResponse, status_code=status.HTTP_201_CREATED)
async def create_track_record(payload: TrackRecordCreate, service: TrackRecordService = Depends(get_track_record_service)):
    try:
        return await service.create_track_record(payload)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.put("/{record_id}", response_model=TrackRecordResponse)
async def update_track_record(record_id: int, payload: TrackRecordUpdate, service: TrackRecordService = Depends(get_track_record_service)):
    try:
        result = await service.update_track_record(record_id, payload)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Track record not found")
    return result


@router.delete("/{record_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_track_record(record_id: int, service: TrackRecordService = Depends(get_track_record_service)):
    deleted = await service.delete_track_record(record_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Track record not found")
