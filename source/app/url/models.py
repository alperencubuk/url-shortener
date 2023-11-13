import uuid

from sqlalchemy import UUID, Column, Integer, String

from source.core.models import Model


class UrlModel(Model):
    __tablename__ = "Urls"

    url = Column(name="url", type_=String)
    shortened_url = Column(
        name="shortened_url", type_=UUID(as_uuid=True), index=True, default=uuid.uuid4
    )
    times_clicked = Column(name="times_clicked", type_=Integer, default=0)
