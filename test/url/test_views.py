import uuid

import pytest
from fastapi import status
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from source.app.url.schemas import UrlPage, UrlResponse
from source.app.url.services import add_url


@pytest.mark.asyncio
async def test_url_add(client: AsyncClient):
    payload = {"url": "https://alperencubuk.com/add"}
    response = await client.post(url="/urls/", json=payload)

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert UrlResponse(**data)
    assert data["url"] == payload["url"]
    assert data["times_clicked"] == 0


@pytest.mark.asyncio
async def test_url_get(client: AsyncClient, db: AsyncSession):
    response = await client.get(url=f"/urls/{uuid.uuid4()}", params={"redirect": False})

    assert response.status_code == status.HTTP_404_NOT_FOUND

    param = "https://alperencubuk.com/get"
    url = await add_url(url=param, db=db)

    response = await client.get(
        url=f"/urls/{url.shortened_url}", params={"redirect": False}
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert UrlResponse(**data)
    assert data["url"] == param


@pytest.mark.asyncio
async def test_url_redirect(client: AsyncClient, db: AsyncSession):
    response = await client.get(url=f"/urls/{uuid.uuid4()}")

    assert response.status_code == status.HTTP_404_NOT_FOUND

    param = "https://alperencubuk.com/redirect"
    url = await add_url(url=param, db=db)

    response = await client.get(url=f"/urls/{url.shortened_url}")

    assert response.status_code == status.HTTP_307_TEMPORARY_REDIRECT
    assert response.headers["location"] == param


@pytest.mark.asyncio
async def test_url_list(client: AsyncClient, db: AsyncSession):
    for i in range(5):
        url = f"https://alperencubuk.com/{i}"
        await add_url(url=url, db=db)

    response = await client.get(url="/urls/", params={"page": 1, "size": 5})

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert UrlPage(**data)
    assert data["urls"] is not None
    assert data["page"] == 1
    assert data["size"] == 5
    assert data["total"] is not None
    assert data["pages"] is not None

    response = await client.get(url="/urls/", params={"page": -5, "size": -5})

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    data = response.json()
    assert data["detail"][0]["loc"][0] == "page"
    assert data["detail"][1]["loc"][0] == "size"


@pytest.mark.asyncio
async def test_url_delete(client: AsyncClient, db: AsyncSession):
    response = await client.delete(url=f"/urls/{uuid.uuid4()}")

    assert response.status_code == status.HTTP_404_NOT_FOUND

    param = "https://alperencubuk.com/delete"
    url = await add_url(url=param, db=db)

    response = await client.delete(url=f"/urls/{url.shortened_url}")

    assert response.status_code == status.HTTP_204_NO_CONTENT
