import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class SaleCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    phone: str = Field(..., min_length=1, max_length=20)
    email: str = Field(..., min_length=1, max_length=100)
    status: str = Field(default="active", pattern=r"^(active|inactive)$")


class SaleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    phone: str
    email: str
    status: str
    created_at: datetime.datetime


class SaleWithAgenciesResponse(SaleResponse):
    agencies: list["AgencyResponse"] = []


class AgencyCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    address: str = Field(..., min_length=1, max_length=255)
    area: str = Field(..., min_length=1, max_length=100)
    sale_id: int = Field(..., gt=0)


class AgencyResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    address: str
    area: str
    sale_id: int
    sale_name: Optional[str] = None
    created_at: datetime.datetime


class AgencyWithRecordsResponse(AgencyResponse):
    track_records: list["TrackRecordResponse"] = []


class TrackRecordCreate(BaseModel):
    customer_name: str = Field(..., min_length=1, max_length=100)
    expected_revenue: float = Field(default=0.0, ge=0)
    status: str = Field(default="new", pattern=r"^(new|contacted|potential|won|lost)$")
    notes: Optional[str] = None
    agency_id: int = Field(..., gt=0)


class TrackRecordResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    customer_name: str
    expected_revenue: float
    status: str
    notes: Optional[str] = None
    agency_id: int
    agency_name: Optional[str] = None
    created_at: datetime.datetime


class StatsResponse(BaseModel):
    active_sales_count: int
    total_agencies: int
    total_track_records: int
    track_records_by_status: dict[str, int]
