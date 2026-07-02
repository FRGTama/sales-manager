class TestStatsEdgeCases:
    async def test_stats_empty_database(self, client):
        response = await client.get("/api/stats")
        assert response.status_code == 200
        data = response.json()
        assert data["active_sales_count"] == 0
        assert data["total_agencies"] == 0
        assert data["total_track_records"] == 0
        assert data["track_records_by_status"] == {}

    async def test_stats_after_sale_created(self, client, created_sale):
        response = await client.get("/api/stats")
        data = response.json()
        assert data["active_sales_count"] == 1
        assert data["total_agencies"] == 0
        assert data["total_track_records"] == 0

    async def test_stats_after_inactive_sale(self, client):
        payload = {"name": "Inactive", "phone": "0909000000", "email": "i@b.com", "status": "inactive"}
        await client.post("/api/sales", json=payload)
        response = await client.get("/api/stats")
        assert response.json()["active_sales_count"] == 0

    async def test_stats_after_agency_created(self, client, created_agency):
        response = await client.get("/api/stats")
        data = response.json()
        assert data["total_agencies"] == 1
        assert data["active_sales_count"] == 1

    async def test_stats_with_multiple_statuses(self, client, created_agency):
        agency_id = created_agency["id"]
        statuses = ["new", "contacted", "potential", "won", "lost"]
        for s in statuses:
            await client.post("/api/track-records", json={
                "customer_name": f"X-{s}", "expected_revenue": 100, "status": s, "agency_id": agency_id,
            })
        response = await client.get("/api/stats")
        data = response.json()
        assert data["total_track_records"] == 5
        assert data["track_records_by_status"] == {"new": 1, "contacted": 1, "potential": 1, "won": 1, "lost": 1}

    async def test_stats_with_multiple_track_records_same_status(self, client, created_agency):
        agency_id = created_agency["id"]
        for _ in range(3):
            await client.post("/api/track-records", json={
                "customer_name": "X", "expected_revenue": 100, "status": "new", "agency_id": agency_id,
            })
        response = await client.get("/api/stats")
        assert response.json()["track_records_by_status"]["new"] == 3
