from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from source.app.url.schemas import (
    DeleteUrlRequest,
    ShortUrlRequest,
    UrlPage,
    UrlPagination,
    UrlRequest,
    UrlResponse,
)
from source.app.url.services import add_url, delete_url, get_url, list_url, url_clicked
from source.core.database import get_db
from source.core.schemas import ExceptionSchema

url_router = APIRouter(prefix="/urls")


@url_router.post(
    "/",
    response_model=UrlResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["urls"],
)
async def url_add(payload: UrlRequest, db: AsyncSession = Depends(get_db)):
    return await add_url(url=payload.url, db=db)


@url_router.get(
    "/{url_path}",
    response_model=UrlResponse,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": ExceptionSchema},
    },
    tags=["urls"],
)
async def url_redirect_or_get(
    background_tasks: BackgroundTasks,
    request: ShortUrlRequest = Depends(),
    db: AsyncSession = Depends(get_db),
):
    if url := await get_url(url=request.url_path, db=db):
        if request.redirect:
            background_tasks.add_task(url_clicked, url=url, db=db)
            return RedirectResponse(url=url.url)
        return url
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Url '{request.url_path}' not found",
    )


@url_router.get(
    "/",
    response_model=UrlPage,
    tags=["urls"],
)
async def url_list(
    pagination: UrlPagination = Depends(),
    db: AsyncSession = Depends(get_db),
):
    return await list_url(
        page=pagination.page,
        size=pagination.size,
        sort=pagination.sort,
        order=pagination.order,
        db=db,
    )


@url_router.delete(
    "/{url_path}",
    responses={
        status.HTTP_404_NOT_FOUND: {"model": ExceptionSchema},
    },
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["urls"],
)
async def url_delete(
    request: DeleteUrlRequest = Depends(),
    db: AsyncSession = Depends(get_db),
):
    if not await delete_url(url=request.url_path, db=db):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Url '{request.url_path}' not found",
        )
