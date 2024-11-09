"""
- Initializing the sheets package
"""
from .add_sheet import AddSheet
from .get_sheet import GetSheet


class SheetsRepo(
    AddSheet,
    GetSheet,
):
    """
    Provides the methods to work with database sheets
    """
