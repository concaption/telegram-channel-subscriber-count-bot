"""
- This module is responsible for representing a telegram worker account in the database
"""
from sqlalchemy import Column, String

from ..base import Base
from ..tables import Tables


class Worker(Base):
    """
    Represents a telegram worker account in the database
    """
    # name of the database table is `workers`
    __tablename__ = Tables.workers

    phone_number = Column(String, primary_key=True)

    def __init__(
        self,
        phone_number: str,
    ):
        self.phone_number = phone_number
