from abc import ABC, abstractmethod
from typing import Optional

from sqlalchemy import func, select, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.models import Agency, Sale, TrackRecord


class SaleRepository(ABC):
    @abstractmethod
    async def list_all(self) -> list[Sale]:
        ...

    @abstractmethod
    async def get_by_id(self, sale_id: int) -> Optional[Sale]:
        ...

    @abstractmethod
    async def create(self, name: str, phone: str, email: str, status: str) -> Sale:
        ...


class AgencyRepository(ABC):
    @abstractmethod
    async def list_all(self) -> list[Agency]:
        ...

    @abstractmethod
    async def get_by_id(self, agency_id: int) -> Optional[Agency]:
        ...

    @abstractmethod
    async def create(self, name: str, address: str, area: str, sale_id: int) -> Agency:
        ...


class TrackRecordRepository(ABC):
    @abstractmethod
    async def list_all(self) -> list[TrackRecord]:
        ...

    @abstractmethod
    async def create(
        self,
        customer_name: str,
        expected_revenue: float,
        status: str,
        notes: Optional[str],
        agency_id: int,
    ) -> TrackRecord:
        ...


class StatsRepository(ABC):
    @abstractmethod
    async def get_active_sales_count(self) -> int:
        ...

    @abstractmethod
    async def get_total_agencies(self) -> int:
        ...

    @abstractmethod
    async def get_total_track_records(self) -> int:
        ...

    @abstractmethod
    async def get_track_records_by_status(self) -> dict[str, int]:
        ...


class SQLSaleRepository(SaleRepository):
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


class SQLAgencyRepository(AgencyRepository):
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


class SQLTrackRecordRepository(TrackRecordRepository):
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


class SQLStatsRepository(StatsRepository):
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
