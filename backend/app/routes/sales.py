from fastapi import APIRouter, Depends, HTTPException, status

from app.schemas import SaleCreate, SaleResponse, SaleWithAgenciesResponse
from app.services import DefaultSaleService, SaleService

router = APIRouter(prefix="/api/sales", tags=["Sales"])


def get_sale_service() -> SaleService:
    raise NotImplementedError("Override via dependencies")


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
