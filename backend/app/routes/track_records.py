from fastapi import APIRouter, Depends, HTTPException, status

from app.schemas import TrackRecordCreate, TrackRecordResponse
from app.services import DefaultTrackRecordService, TrackRecordService

router = APIRouter(prefix="/api/track-records", tags=["Track Records"])


def get_track_record_service() -> TrackRecordService:
    raise NotImplementedError("Override via dependencies")


@router.get("", response_model=list[TrackRecordResponse])
async def list_track_records(service: TrackRecordService = Depends(get_track_record_service)):
    return await service.list_track_records()


@router.post("", response_model=TrackRecordResponse, status_code=status.HTTP_201_CREATED)
async def create_track_record(payload: TrackRecordCreate, service: TrackRecordService = Depends(get_track_record_service)):
    try:
        return await service.create_track_record(payload)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
