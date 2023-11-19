import uuid

from pydantic import UUID4
from sqlalchemy.orm import Mapped, mapped_column

from source.core.models import Model


class UrlModel(Model):
    __tablename__ = "Urls"

    url: Mapped[str]
    shortened_url: Mapped[UUID4] = mapped_column(
        default=uuid.uuid4, index=True, unique=True
    )
    times_clicked: Mapped[int] = mapped_column(default=0)
