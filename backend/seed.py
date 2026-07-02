import asyncio
import os

from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.models import Agency, Sale, TrackRecord


async def seed():
    engine = create_async_engine(os.environ["DATABASE_URL"])

    async with async_sessionmaker(engine, expire_on_commit=False)() as session:
        await session.execute(
            text("TRUNCATE TABLE sales, agencies, track_records RESTART IDENTITY CASCADE")
        )

        alice = Sale(
            name="Alice Nguyen",
            phone="0909123456",
            email="alice@example.com",
            status="active",
        )
        bob = Sale(
            name="Bob Tran",
            phone="0909987654",
            email="bob@example.com",
            status="inactive",
        )
        session.add_all([alice, bob])
        await session.flush()

        agencies = [
            Agency(name="Hanoi Agency", address="123 Kim Ma", area="Hà Nội", sale_id=alice.id),
            Agency(
                name="Saigon Partners",
                address="456 Le Loi",
                area="Hồ Chí Minh City",
                sale_id=alice.id,
            ),
            Agency(
                name="Da Nang Media", address="789 Bach Dang", area="Đà Nẵng", sale_id=bob.id
            ),
        ]
        session.add_all(agencies)
        await session.flush()

        records = [
            TrackRecord(
                customer_name="Tech Corp",
                expected_revenue=50000,
                status="new",
                notes="Initial contact",
                agency_id=agencies[0].id,
            ),
            TrackRecord(
                customer_name="Green Inc",
                expected_revenue=120000,
                status="won",
                notes="Signed contract",
                agency_id=agencies[0].id,
            ),
            TrackRecord(
                customer_name="Blue Solutions",
                expected_revenue=30000,
                status="contacted",
                notes="Follow-up scheduled",
                agency_id=agencies[1].id,
            ),
            TrackRecord(
                customer_name="Red Ventures",
                expected_revenue=75000,
                status="potential",
                notes="Interested in partnership",
                agency_id=agencies[1].id,
            ),
            TrackRecord(
                customer_name="Yellow Labs",
                expected_revenue=20000,
                status="lost",
                notes="Chose competitor",
                agency_id=agencies[2].id,
            ),
        ]
        session.add_all(records)
        await session.commit()
        print(f"Seeded: 2 sales, {len(agencies)} agencies, {len(records)} track records")


if __name__ == "__main__":
    asyncio.run(seed())
