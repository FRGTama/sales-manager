from typing import Optional

from app.repositories import (
    AgencyRepository,
    SaleRepository,
    StatsRepository,
    TrackRecordRepository,
)
from app.schemas import (
    AgencyCreate,
    AgencyResponse,
    AgencyUpdate,
    AgencyWithRecordsResponse,
    SaleCreate,
    SaleResponse,
    SaleUpdate,
    SaleWithAgenciesResponse,
    StatsResponse,
    TrackRecordCreate,
    TrackRecordResponse,
    TrackRecordUpdate,
)


class SaleService:
    def __init__(self, sale_repo: SaleRepository, agency_repo: AgencyRepository):
        self._sale_repo = sale_repo
        self._agency_repo = agency_repo

    async def list_sales(self) -> list[SaleResponse]:
        sales = await self._sale_repo.list_all()
        return [SaleResponse.model_validate(s) for s in sales]

    async def get_sale(self, sale_id: int) -> Optional[SaleWithAgenciesResponse]:
        sale = await self._sale_repo.get_by_id(sale_id)
        if not sale:
            return None
        return SaleWithAgenciesResponse.model_validate(sale)

    async def create_sale(self, payload: SaleCreate) -> SaleResponse:
        sale = await self._sale_repo.create(
            name=payload.name,
            phone=payload.phone,
            email=payload.email,
            status=payload.status,
        )
        return SaleResponse.model_validate(sale)

    async def update_sale(self, sale_id: int, payload: SaleUpdate) -> Optional[SaleResponse]:
        sale = await self._sale_repo.update(
            sale_id=sale_id,
            name=payload.name,
            phone=payload.phone,
            email=payload.email,
            status=payload.status,
        )
        if not sale:
            return None
        return SaleResponse.model_validate(sale)

    async def delete_sale(self, sale_id: int) -> bool:
        return await self._sale_repo.delete(sale_id)


class AgencyService:
    def __init__(self, agency_repo: AgencyRepository, sale_repo: SaleRepository):
        self._agency_repo = agency_repo
        self._sale_repo = sale_repo

    async def list_agencies(self) -> list[AgencyResponse]:
        agencies = await self._agency_repo.list_all()
        return [
            AgencyResponse(
                id=a.id,
                name=a.name,
                address=a.address,
                area=a.area,
                sale_id=a.sale_id,
                sale_name=getattr(a, "_sale_name", None),
                created_at=a.created_at,
            )
            for a in agencies
        ]

    async def get_agency(self, agency_id: int) -> Optional[AgencyWithRecordsResponse]:
        agency = await self._agency_repo.get_by_id(agency_id)
        if not agency:
            return None
        return AgencyWithRecordsResponse.model_validate(agency)

    async def create_agency(self, payload: AgencyCreate) -> AgencyResponse:
        sale = await self._sale_repo.get_by_id(payload.sale_id)
        if not sale:
            raise ValueError(f"Sale with id {payload.sale_id} not found")
        agency = await self._agency_repo.create(
            name=payload.name,
            address=payload.address,
            area=payload.area,
            sale_id=payload.sale_id,
        )
        return AgencyResponse(
            id=agency.id,
            name=agency.name,
            address=agency.address,
            area=agency.area,
            sale_id=agency.sale_id,
            sale_name=sale.name,
            created_at=agency.created_at,
        )

    async def update_agency(
        self, agency_id: int, payload: AgencyUpdate
    ) -> Optional[AgencyResponse]:
        sale = await self._sale_repo.get_by_id(payload.sale_id)
        if not sale:
            raise ValueError(f"Sale with id {payload.sale_id} not found")
        agency = await self._agency_repo.update(
            agency_id=agency_id,
            name=payload.name,
            address=payload.address,
            area=payload.area,
            sale_id=payload.sale_id,
        )
        if not agency:
            return None
        return AgencyResponse(
            id=agency.id,
            name=agency.name,
            address=agency.address,
            area=agency.area,
            sale_id=agency.sale_id,
            sale_name=sale.name,
            created_at=agency.created_at,
        )

    async def delete_agency(self, agency_id: int) -> bool:
        return await self._agency_repo.delete(agency_id)


class TrackRecordService:
    def __init__(self, record_repo: TrackRecordRepository, agency_repo: AgencyRepository):
        self._record_repo = record_repo
        self._agency_repo = agency_repo

    async def list_track_records(self) -> list[TrackRecordResponse]:
        records = await self._record_repo.list_all()
        return [
            TrackRecordResponse(
                id=r.id,
                customer_name=r.customer_name,
                expected_revenue=r.expected_revenue,
                status=r.status,
                notes=r.notes,
                agency_id=r.agency_id,
                agency_name=getattr(r, "_agency_name", None),
                created_at=r.created_at,
            )
            for r in records
        ]

    async def create_track_record(self, payload: TrackRecordCreate) -> TrackRecordResponse:
        agency = await self._agency_repo.get_by_id(payload.agency_id)
        if not agency:
            raise ValueError(f"Agency with id {payload.agency_id} not found")
        record = await self._record_repo.create(
            customer_name=payload.customer_name,
            expected_revenue=payload.expected_revenue,
            status=payload.status,
            notes=payload.notes,
            agency_id=payload.agency_id,
        )
        return TrackRecordResponse(
            id=record.id,
            customer_name=record.customer_name,
            expected_revenue=record.expected_revenue,
            status=record.status,
            notes=record.notes,
            agency_id=record.agency_id,
            agency_name=agency.name,
            created_at=record.created_at,
        )

    async def update_track_record(
        self, record_id: int, payload: TrackRecordUpdate
    ) -> Optional[TrackRecordResponse]:
        agency = await self._agency_repo.get_by_id(payload.agency_id)
        if not agency:
            raise ValueError(f"Agency with id {payload.agency_id} not found")
        record = await self._record_repo.update(
            record_id=record_id,
            customer_name=payload.customer_name,
            expected_revenue=payload.expected_revenue,
            status=payload.status,
            notes=payload.notes,
            agency_id=payload.agency_id,
        )
        if not record:
            return None
        return TrackRecordResponse(
            id=record.id,
            customer_name=record.customer_name,
            expected_revenue=record.expected_revenue,
            status=record.status,
            notes=record.notes,
            agency_id=record.agency_id,
            agency_name=agency.name,
            created_at=record.created_at,
        )

    async def delete_track_record(self, record_id: int) -> bool:
        return await self._record_repo.delete(record_id)


class StatsService:
    def __init__(self, stats_repo: StatsRepository):
        self._stats_repo = stats_repo

    async def get_stats(self) -> StatsResponse:
        active_sales = await self._stats_repo.get_active_sales_count()
        total_agencies = await self._stats_repo.get_total_agencies()
        total_records = await self._stats_repo.get_total_track_records()
        by_status = await self._stats_repo.get_track_records_by_status()
        return StatsResponse(
            active_sales_count=active_sales,
            total_agencies=total_agencies,
            total_track_records=total_records,
            track_records_by_status=by_status,
        )
