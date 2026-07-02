import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    phone = Column(String(10), nullable=False)
    email = Column(String(100), nullable=False)
    status = Column(String(20), nullable=False, default="active")
    created_at = Column(DateTime, nullable=False, server_default=func.now())

    agencies = relationship("Agency", back_populates="sale", cascade="all, delete-orphan")


class Agency(Base):
    __tablename__ = "agencies"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    address = Column(String(255), nullable=False)
    area = Column(String(100), nullable=False)
    sale_id = Column(Integer, ForeignKey("sales.id"), nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())

    sale = relationship("Sale", back_populates="agencies")
    track_records = relationship("TrackRecord", back_populates="agency", cascade="all, delete-orphan")


class TrackRecord(Base):
    __tablename__ = "track_records"

    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_name = Column(String(100), nullable=False)
    expected_revenue = Column(Float, nullable=False, default=0.0)
    status = Column(String(20), nullable=False, default="new")
    notes = Column(Text, nullable=True)
    agency_id = Column(Integer, ForeignKey("agencies.id"), nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())

    agency = relationship("Agency", back_populates="track_records")
