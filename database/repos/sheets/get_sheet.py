"""
- This module is responsible for providing the methods to get sheets from the database
"""
from typing import Union

from sqlalchemy.orm import Session

from ... import models


sheet_type = "models.sheets.Sheet"


class GetSheet:
    """
    Provides the method to get chats from the database
    """
    @staticmethod
    def get_sheet(session: Session) -> Union[sheet_type, None]:
        """
        Returns the first sheet from the database
        """
        sheet_cls = models.sheets.Sheet
        sheet = session.query(sheet_cls).one_or_none()
        return sheet
