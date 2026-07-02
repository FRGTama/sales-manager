import pytest


class TestTrackRecordsEdgeCases:
    async def test_create_track_record_empty_customer(self, client, created_agency):
        payload = {"customer_name": "", "expected_revenue": 100, "status": "new", "agency_id": created_agency["id"]}
        response = await client.post("/api/track-records", json=payload)
        assert response.status_code == 422

    async def test_create_track_record_negative_revenue(self, client, created_agency):
        payload = {"customer_name": "X", "expected_revenue": -100, "status": "new", "agency_id": created_agency["id"]}
        response = await client.post("/api/track-records", json=payload)
        assert response.status_code == 422

    async def test_create_track_record_zero_revenue(self, client, created_agency):
        payload = {"customer_name": "X", "expected_revenue": 0, "status": "new", "agency_id": created_agency["id"]}
        response = await client.post("/api/track-records", json=payload)
        assert response.status_code == 201

    async def test_create_track_record_invalid_status(self, client, created_agency):
        payload = {"customer_name": "X", "expected_revenue": 100, "status": "invalid", "agency_id": created_agency["id"]}
        response = await client.post("/api/track-records", json=payload)
        assert response.status_code == 422

    @pytest.mark.parametrize("status", ["new", "contacted", "potential", "won", "lost"])
    async def test_create_track_record_valid_statuses(self, client, created_agency, status):
        payload = {"customer_name": "X", "expected_revenue": 100, "status": status, "agency_id": created_agency["id"]}
        response = await client.post("/api/track-records", json=payload)
        assert response.status_code == 201
        assert response.json()["status"] == status

    async def test_create_track_record_invalid_agency_id(self, client):
        payload = {"customer_name": "X", "expected_revenue": 100, "status": "new", "agency_id": 999}
        response = await client.post("/api/track-records", json=payload)
        assert response.status_code == 404

    async def test_create_track_record_zero_agency_id(self, client):
        payload = {"customer_name": "X", "expected_revenue": 100, "status": "new", "agency_id": 0}
        response = await client.post("/api/track-records", json=payload)
        assert response.status_code == 422

    async def test_create_track_record_negative_agency_id(self, client):
        payload = {"customer_name": "X", "expected_revenue": 100, "status": "new", "agency_id": -1}
        response = await client.post("/api/track-records", json=payload)
        assert response.status_code == 422

    async def test_create_track_record_null_notes(self, client, created_agency):
        payload = {"customer_name": "X", "expected_revenue": 100, "status": "new", "notes": None, "agency_id": created_agency["id"]}
        response = await client.post("/api/track-records", json=payload)
        assert response.status_code == 201
        assert response.json()["notes"] is None

    async def test_create_track_record_with_notes(self, client, created_agency):
        payload = {"customer_name": "X", "expected_revenue": 100, "status": "new", "notes": "Some notes", "agency_id": created_agency["id"]}
        response = await client.post("/api/track-records", json=payload)
        assert response.status_code == 201
        assert response.json()["notes"] == "Some notes"

    async def test_list_track_records_empty(self, client):
        response = await client.get("/api/track-records")
        assert response.status_code == 200
        assert response.json() == []

    async def test_list_track_records_contains_agency_name(self, client, created_track_record):
        response = await client.get("/api/track-records")
        data = response.json()
        assert len(data) == 1
        assert data[0]["agency_name"] is not None

    async def test_create_track_record_with_high_revenue(self, client, created_agency):
        payload = {"customer_name": "Big Deal", "expected_revenue": 1_000_000_000, "status": "potential", "agency_id": created_agency["id"]}
        response = await client.post("/api/track-records", json=payload)
        assert response.status_code == 201
        assert response.json()["expected_revenue"] == 1_000_000_000.0

    async def test_create_track_record_with_float_revenue(self, client, created_agency):
        payload = {"customer_name": "X", "expected_revenue": 99.99, "status": "new", "agency_id": created_agency["id"]}
        response = await client.post("/api/track-records", json=payload)
        assert response.status_code == 201
        assert response.json()["expected_revenue"] == 99.99
