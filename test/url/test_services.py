import uuid

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from source.app.url.enums import Order, Sort
from source.app.url.services import add_url, delete_url, get_url, list_url, url_clicked


@pytest.mark.asyncio
async def test_add_url(db: AsyncSession):
    url = "https://alperencubuk.com/add"
    result = await add_url(url=url, db=db)
    assert result is not None
    assert result.url == url


@pytest.mark.asyncio
async def test_get_url(db):
    url = "https://alperencubuk.com/get"
    result = await add_url(url=url, db=db)

    retrieved_url = await get_url(url=result.shortened_url, db=db)
    assert retrieved_url is not None
    assert retrieved_url.url == url


@pytest.mark.asyncio
async def test_list_url(db):
    for i in range(5):
        url = f"https://alperencubuk.com/{i}"
        await add_url(url=url, db=db)
    result = await list_url(page=1, size=5, sort=Sort.ID, order=Order.DESC, db=db)
    assert result is not None
    assert result.urls is not None
    assert result.page == 1
    assert result.size == 5
    assert result.total is not None
    assert result.pages is not None


@pytest.mark.asyncio
async def test_delete_url(db):
    url = "https://alperencubuk.com/delete"
    result = await add_url(url=url, db=db)
    assert result is not None

    delete_result = await delete_url(url=result.shortened_url, db=db)
    assert delete_result is True

    delete_result = await delete_url(url=uuid.uuid4(), db=db)
    assert delete_result is False


@pytest.mark.asyncio
async def test_url_clicked(db):
    url = "https://alperencubuk.com/clicked"
    result = await add_url(url=url, db=db)
    assert result is not None
    times_clicked = result.times_clicked

    await url_clicked(url=result, db=db)

    updated_result = await get_url(url=result.shortened_url, db=db)
    assert updated_result is not None
    assert updated_result.times_clicked == times_clicked + 1
