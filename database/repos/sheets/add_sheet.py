"""
- This module is responsible for providing the method to add sheets
"""
from typing import Union

from sqlalchemy.orm import Session

from .. import sheets
from ... import models


sheet_type = "models.sheets.Sheet"


class AddSheet:
    """
    Provides the method to Add sheets to the database
    """
    @classmethod
    def add_sheet(cls: "sheets.SheetsRepo", sheet_url: str, session: Session) -> Union:
        """
        Adds the sheet to the database
        """
        sheet_cls = models.sheets.Sheet
        db_sheet = cls.get_sheet(session)
        if db_sheet is not None:
            session.delete(db_sheet)

        db_sheet = sheet_cls(
            url=sheet_url,
        )
        session.add(db_sheet)

        return db_sheet
