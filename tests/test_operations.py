from httpx import AsyncClient


async def test_add_specific_operations(ac: AsyncClient):
    response = await ac.post("/operations/post", json={
                              "id": 1,
                              "quantity": "231.3",
                              "figi": "figi_code",
                              "instrument_type": "instrument_type",
                              "date": "2023-10-29T22:25:40.104",
                              "type": "operation_type"
                            })
    assert response.status_code == 200


async def test_get_specific_operations(ac: AsyncClient):
    response = await ac.get("/operations/get", params={
        "operation_type": "operation_type"
    })
    assert response.status_code == 200
    assert response.json()["status"] == 'success'
    assert len(response.json()['data']) == 1
