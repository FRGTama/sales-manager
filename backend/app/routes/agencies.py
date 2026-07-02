from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.repositories import AgencyRepository, SaleRepository
from app.schemas import AgencyCreate, AgencyResponse, AgencyUpdate, AgencyWithRecordsResponse
from app.services import AgencyService

router = APIRouter(prefix="/api/agencies", tags=["Agencies"])


async def get_agency_service(db: AsyncSession = Depends(get_db)) -> AgencyService:
    return AgencyService(AgencyRepository(db), SaleRepository(db))


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


@router.put("/{agency_id}", response_model=AgencyResponse)
async def update_agency(agency_id: int, payload: AgencyUpdate, service: AgencyService = Depends(get_agency_service)):
    try:
        result = await service.update_agency(agency_id, payload)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agency not found")
    return result


@router.delete("/{agency_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_agency(agency_id: int, service: AgencyService = Depends(get_agency_service)):
    deleted = await service.delete_agency(agency_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agency not found")
