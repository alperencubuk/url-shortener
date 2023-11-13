import pytest
from fastapi import status
from httpx import AsyncClient

from source.core.schemas import HealthSchema


@pytest.mark.asyncio
async def test_health_check(client: AsyncClient):
    response = await client.get(url="/")

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert HealthSchema(**data)
    assert data["api"] is True
    assert data["database"] is True
