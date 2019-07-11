

async def test_status_api(client):
    response = await client.get("/status")
    assert response.status == 200
    assert response.content_type == "application/json"
    assert dict(status="OK") == await response.json()
