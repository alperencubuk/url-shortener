from datetime import datetime
from typing import Any

from fastapi import HTTPException, status
from pydantic import UUID4, BaseModel, Field, HttpUrl, ValidationError, model_validator

from source.app.url.enums import Order, Sort
from source.core.schemas import PageSchema, ResponseSchema
from source.core.settings import settings


class UrlRequest(BaseModel):
    url: HttpUrl


class ShortUrlRequest(BaseModel):
    url_path: UUID4
    redirect: bool = True


class DeleteUrlRequest(BaseModel):
    url_path: UUID4


class UrlResponse(ResponseSchema):
    url: HttpUrl
    shortened_url: UUID4 | str
    times_clicked: int
    create_date: datetime

    @model_validator(mode="after")
    def validator(cls, values: "UrlResponse") -> "UrlResponse":
        values.shortened_url = f"{settings.BASE_URL}/urls/{values.shortened_url}"
        return values


class UrlPage(PageSchema):
    urls: list[UrlResponse]


class UrlPagination(BaseModel):
    page: int = Field(default=1, ge=1)
    size: int = Field(default=50, ge=1)
    sort: Sort = Sort.ID
    order: Order = Order.ASC

    def __init__(self, **data: Any) -> None:
        try:
            super(UrlPagination, self).__init__(**data)
        except ValidationError as error:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=error.errors(),
            )
