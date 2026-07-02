from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.repositories import SaleRepository, AgencyRepository
from app.schemas import SaleCreate, SaleResponse, SaleUpdate, SaleWithAgenciesResponse
from app.services import SaleService

router = APIRouter(prefix="/api/sales", tags=["Sales"])


async def get_sale_service(db: AsyncSession = Depends(get_db)) -> SaleService:
    return SaleService(SaleRepository(db), AgencyRepository(db))


@router.get("", response_model=list[SaleResponse])
async def list_sales(service: SaleService = Depends(get_sale_service)):
    return await service.list_sales()


@router.post("", response_model=SaleResponse, status_code=status.HTTP_201_CREATED)
async def create_sale(payload: SaleCreate, service: SaleService = Depends(get_sale_service)):
    return await service.create_sale(payload)


@router.get("/{sale_id}", response_model=SaleWithAgenciesResponse)
async def get_sale(sale_id: int, service: SaleService = Depends(get_sale_service)):
    result = await service.get_sale(sale_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sale not found")
    return result


@router.put("/{sale_id}", response_model=SaleResponse)
async def update_sale(sale_id: int, payload: SaleUpdate, service: SaleService = Depends(get_sale_service)):
    result = await service.update_sale(sale_id, payload)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sale not found")
    return result


@router.delete("/{sale_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_sale(sale_id: int, service: SaleService = Depends(get_sale_service)):
    deleted = await service.delete_sale(sale_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sale not found")
