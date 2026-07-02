from typing import Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.models import Agency, Sale, TrackRecord


class SaleRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def list_all(self) -> list[Sale]:
        result = await self._session.execute(select(Sale).order_by(Sale.created_at.desc()))
        return list(result.scalars().all())

    async def get_by_id(self, sale_id: int) -> Optional[Sale]:
        result = await self._session.execute(
            select(Sale).where(Sale.id == sale_id).options(joinedload(Sale.agencies))
        )
        return result.unique().scalar_one_or_none()

    async def create(self, name: str, phone: str, email: str, status: str) -> Sale:
        sale = Sale(name=name, phone=phone, email=email, status=status)
        self._session.add(sale)
        await self._session.flush()
        return sale

    async def update(
        self, sale_id: int, name: str, phone: str, email: str, status: str
    ) -> Optional[Sale]:
        sale = await self._session.get(Sale, sale_id)
        if not sale:
            return None
        sale.name = name
        sale.phone = phone
        sale.email = email
        sale.status = status
        await self._session.flush()
        return sale

    async def delete(self, sale_id: int) -> bool:
        sale = await self._session.get(Sale, sale_id)
        if not sale:
            return False
        await self._session.delete(sale)
        await self._session.flush()
        return True


class AgencyRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def list_all(self) -> list[Agency]:
        result = await self._session.execute(
            select(Agency, Sale.name.label("sale_name"))
            .join(Sale, Agency.sale_id == Sale.id)
            .order_by(Agency.created_at.desc())
        )
        rows = result.all()
        agencies = []
        for agency, sale_name in rows:
            agency._sale_name = sale_name
            agencies.append(agency)
        return agencies

    async def get_by_id(self, agency_id: int) -> Optional[Agency]:
        result = await self._session.execute(
            select(Agency)
            .where(Agency.id == agency_id)
            .options(joinedload(Agency.track_records))
        )
        return result.unique().scalar_one_or_none()

    async def create(self, name: str, address: str, area: str, sale_id: int) -> Agency:
        agency = Agency(name=name, address=address, area=area, sale_id=sale_id)
        self._session.add(agency)
        await self._session.flush()
        return agency

    async def update(
        self, agency_id: int, name: str, address: str, area: str, sale_id: int
    ) -> Optional[Agency]:
        agency = await self._session.get(Agency, agency_id)
        if not agency:
            return None
        agency.name = name
        agency.address = address
        agency.area = area
        agency.sale_id = sale_id
        await self._session.flush()
        return agency

    async def delete(self, agency_id: int) -> bool:
        agency = await self._session.get(Agency, agency_id)
        if not agency:
            return False
        await self._session.delete(agency)
        await self._session.flush()
        return True


class TrackRecordRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def list_all(self) -> list[TrackRecord]:
        result = await self._session.execute(
            select(TrackRecord, Agency.name.label("agency_name"))
            .join(Agency, TrackRecord.agency_id == Agency.id)
            .order_by(TrackRecord.created_at.desc())
        )
        rows = result.all()
        records = []
        for record, agency_name in rows:
            record._agency_name = agency_name
            records.append(record)
        return records

    async def create(
        self,
        customer_name: str,
        expected_revenue: float,
        status: str,
        notes: Optional[str],
        agency_id: int,
    ) -> TrackRecord:
        record = TrackRecord(
            customer_name=customer_name,
            expected_revenue=expected_revenue,
            status=status,
            notes=notes,
            agency_id=agency_id,
        )
        self._session.add(record)
        await self._session.flush()
        return record

    async def update(
        self,
        record_id: int,
        customer_name: str,
        expected_revenue: float,
        status: str,
        notes: Optional[str],
        agency_id: int,
    ) -> Optional[TrackRecord]:
        record = await self._session.get(TrackRecord, record_id)
        if not record:
            return None
        record.customer_name = customer_name
        record.expected_revenue = expected_revenue
        record.status = status
        record.notes = notes
        record.agency_id = agency_id
        await self._session.flush()
        return record

    async def delete(self, record_id: int) -> bool:
        record = await self._session.get(TrackRecord, record_id)
        if not record:
            return False
        await self._session.delete(record)
        await self._session.flush()
        return True


class StatsRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_active_sales_count(self) -> int:
        result = await self._session.execute(
            select(func.count(Sale.id)).where(Sale.status == "active")
        )
        return result.scalar() or 0

    async def get_total_agencies(self) -> int:
        result = await self._session.execute(select(func.count(Agency.id)))
        return result.scalar() or 0

    async def get_total_track_records(self) -> int:
        result = await self._session.execute(select(func.count(TrackRecord.id)))
        return result.scalar() or 0

    async def get_track_records_by_status(self) -> dict[str, int]:
        result = await self._session.execute(
            select(TrackRecord.status, func.count(TrackRecord.id)).group_by(TrackRecord.status)
        )
        return {row[0]: row[1] for row in result.all()}
