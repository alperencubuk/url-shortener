from uuid import UUID

from pydantic import HttpUrl
from sqlalchemy import asc, desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from source.app.url.enums import Order, Sort
from source.app.url.models import UrlModel
from source.app.url.schemas import UrlPage


async def add_url(url: HttpUrl, db: AsyncSession) -> UrlModel:
    url = UrlModel(url=str(url))
    db.add(url)
    await db.commit()
    await db.refresh(url)
    return url


async def get_url(url: UUID, db: AsyncSession) -> UrlModel | None:
    return await db.scalar(select(UrlModel).filter(UrlModel.shortened_url == url))


async def list_url(
    page: int, size: int, sort: Sort, order: Order, db: AsyncSession
) -> UrlPage:
    order = asc(sort) if order == Order.ASC else desc(sort)
    urls = await db.scalars(
        select(UrlModel).order_by(order).offset((page - 1) * size).limit(size)
    )
    total = await db.scalar(select(func.count(UrlModel.id)))

    return UrlPage(
        urls=urls,
        page=page,
        size=size,
        total=total,
        pages=((total + size - 1) // size if size else 1),
    )


async def delete_url(url: UUID, db: AsyncSession) -> bool:
    if response := await get_url(url=url, db=db):
        await db.delete(response)
        await db.commit()
        return True
    return False


async def url_clicked(url: UrlModel, db: AsyncSession) -> None:
    url.times_clicked += 1
    await db.commit()
    await db.refresh(url)
