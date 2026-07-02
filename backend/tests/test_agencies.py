import pytest


class TestAgenciesEdgeCases:
    async def test_create_agency_empty_name(self, client, created_sale):
        payload = {"name": "", "address": "Addr", "area": "Area", "sale_id": created_sale["id"]}
        response = await client.post("/api/agencies", json=payload)
        assert response.status_code == 422

    async def test_create_agency_empty_address(self, client, created_sale):
        payload = {"name": "Agency", "address": "", "area": "Area", "sale_id": created_sale["id"]}
        response = await client.post("/api/agencies", json=payload)
        assert response.status_code == 422

    async def test_create_agency_empty_area(self, client, created_sale):
        payload = {"name": "Agency", "address": "Addr", "area": "", "sale_id": created_sale["id"]}
        response = await client.post("/api/agencies", json=payload)
        assert response.status_code == 422

    async def test_create_agency_invalid_sale_id(self, client):
        payload = {"name": "Agency", "address": "Addr", "area": "HCMC", "sale_id": 999}
        response = await client.post("/api/agencies", json=payload)
        assert response.status_code == 404

    async def test_create_agency_zero_sale_id(self, client):
        payload = {"name": "Agency", "address": "Addr", "area": "HCMC", "sale_id": 0}
        response = await client.post("/api/agencies", json=payload)
        assert response.status_code == 422

    async def test_create_agency_negative_sale_id(self, client):
        payload = {"name": "Agency", "address": "Addr", "area": "HCMC", "sale_id": -1}
        response = await client.post("/api/agencies", json=payload)
        assert response.status_code == 422

    async def test_create_agency_success(self, client, created_sale):
        payload = {"name": "Agency A", "address": "123 Street", "area": "HCMC", "sale_id": created_sale["id"]}
        response = await client.post("/api/agencies", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Agency A"
        assert data["sale_name"] == created_sale["name"]

    async def test_list_agencies_empty(self, client):
        response = await client.get("/api/agencies")
        assert response.status_code == 200
        assert response.json() == []

    async def test_list_agencies_contains_sale_name(self, client, created_agency):
        response = await client.get("/api/agencies")
        data = response.json()
        assert len(data) == 1
        assert data[0]["sale_name"] is not None

    async def test_get_agency_not_found(self, client):
        response = await client.get("/api/agencies/999")
        assert response.status_code == 404

    async def test_get_agency_with_track_records(self, client, created_agency, created_track_record):
        agency_id = created_agency["id"]
        response = await client.get(f"/api/agencies/{agency_id}")
        data = response.json()
        assert "track_records" in data
        assert len(data["track_records"]) == 1
        assert data["track_records"][0]["id"] == created_track_record["id"]

    async def test_create_agency_long_name(self, client, created_sale):
        payload = {"name": "A" * 100, "address": "Addr", "area": "Area", "sale_id": created_sale["id"]}
        response = await client.post("/api/agencies", json=payload)
        assert response.status_code == 201

    async def test_create_agency_name_too_long(self, client, created_sale):
        payload = {"name": "A" * 101, "address": "Addr", "area": "Area", "sale_id": created_sale["id"]}
        response = await client.post("/api/agencies", json=payload)
        assert response.status_code == 422
