import pytest


class TestSalesEdgeCases:
    async def test_create_sale_empty_name(self, client):
        payload = {"name": "", "phone": "0909123456", "email": "a@b.com", "status": "active"}
        response = await client.post("/api/sales", json=payload)
        assert response.status_code == 422

    async def test_create_sale_empty_phone(self, client):
        payload = {"name": "Alice", "phone": "", "email": "a@b.com", "status": "active"}
        response = await client.post("/api/sales", json=payload)
        assert response.status_code == 422

    async def test_create_sale_empty_email(self, client):
        payload = {"name": "Alice", "phone": "0909123456", "email": "", "status": "active"}
        response = await client.post("/api/sales", json=payload)
        assert response.status_code == 422

    async def test_create_sale_invalid_status(self, client):
        payload = {"name": "Alice", "phone": "0909123456", "email": "a@b.com", "status": "bogus"}
        response = await client.post("/api/sales", json=payload)
        assert response.status_code == 422

    @pytest.mark.parametrize("status", ["active", "inactive"])
    async def test_create_sale_valid_statuses(self, client, status):
        payload = {"name": "Alice", "phone": "0909123456", "email": "a@b.com", "status": status}
        response = await client.post("/api/sales", json=payload)
        assert response.status_code == 201
        assert response.json()["status"] == status

    async def test_create_sale_minimal_valid(self, client):
        payload = {"name": "Bob", "phone": "0909000000", "email": "bob@example.com"}
        response = await client.post("/api/sales", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Bob"
        assert data["status"] == "active"

    async def test_create_sale_long_name(self, client):
        payload = {"name": "A" * 100, "phone": "0909123456", "email": "a@b.com", "status": "active"}
        response = await client.post("/api/sales", json=payload)
        assert response.status_code == 201

    async def test_create_sale_name_too_long(self, client):
        payload = {"name": "A" * 101, "phone": "0909123456", "email": "a@b.com", "status": "active"}
        response = await client.post("/api/sales", json=payload)
        assert response.status_code == 422

    async def test_list_sales_empty(self, client):
        response = await client.get("/api/sales")
        assert response.status_code == 200
        assert response.json() == []

    async def test_list_sales_after_creation(self, client, created_sale):
        response = await client.get("/api/sales")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        assert data[0]["name"] == created_sale["name"]

    async def test_get_sale_not_found(self, client):
        response = await client.get("/api/sales/999")
        assert response.status_code == 404

    async def test_get_sale_success(self, client, created_sale):
        sale_id = created_sale["id"]
        response = await client.get(f"/api/sales/{sale_id}")
        assert response.status_code == 200
        assert response.json()["id"] == sale_id

    async def test_get_sale_with_agencies(self, client, created_sale, created_agency):
        sale_id = created_sale["id"]
        response = await client.get(f"/api/sales/{sale_id}")
        data = response.json()
        assert "agencies" in data
        assert len(data["agencies"]) == 1
        assert data["agencies"][0]["id"] == created_agency["id"]

    async def test_create_sale_duplicate_email_allowed(self, client, created_sale):
        payload = {"name": "Clone", "phone": "0909000000", "email": created_sale["email"], "status": "active"}
        response = await client.post("/api/sales", json=payload)
        assert response.status_code == 201
