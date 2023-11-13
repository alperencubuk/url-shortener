from sqlalchemy import Column, DateTime, Integer, func

from source.core.database import Base


class Model(Base):
    __abstract__ = True

    id = Column(name="id", type_=Integer, primary_key=True, autoincrement=True)
    create_date = Column(name="create_date", type_=DateTime, default=func.now())
