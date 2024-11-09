"""
- This module is responsible for representing sheets in the database
"""
from sqlalchemy import Column, Integer, String

from ..base import Base
from ..tables import Tables


class Sheet(Base):
    """
    Represents a sheet in the database
    """
    # the name of the table is `sheets`
    __tablename__ = Tables.sheets

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String, nullable=False)

    def __init__(
        self,
        url: str,
    ):
        self.url = url
