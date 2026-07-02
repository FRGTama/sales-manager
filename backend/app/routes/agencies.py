from fastapi import APIRouter, Depends, HTTPException, status

from app.schemas import AgencyCreate, AgencyResponse, AgencyWithRecordsResponse
from app.services import AgencyService, DefaultAgencyService

router = APIRouter(prefix="/api/agencies", tags=["Agencies"])


def get_agency_service() -> AgencyService:
    raise NotImplementedError("Override via dependencies")


@router.get("", response_model=list[AgencyResponse])
async def list_agencies(service: AgencyService = Depends(get_agency_service)):
    return await service.list_agencies()


@router.post("", response_model=AgencyResponse, status_code=status.HTTP_201_CREATED)
async def create_agency(payload: AgencyCreate, service: AgencyService = Depends(get_agency_service)):
    try:
        return await service.create_agency(payload)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/{agency_id}", response_model=AgencyWithRecordsResponse)
async def get_agency(agency_id: int, service: AgencyService = Depends(get_agency_service)):
    result = await service.get_agency(agency_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agency not found")
    return result
