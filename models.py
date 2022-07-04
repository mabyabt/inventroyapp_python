from sqlalchemy import Boolean, Column, Integer, String

from database import Base


class Inventory(Base):
    __tablename__ = "invetory"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    quantity = Column(Integer, default=0)

