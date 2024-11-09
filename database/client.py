"""
- This module is responsible for defining the DbClient class
"""
from .repos import (
    chats,
    sheets,
    workers,
)


class DbClient(
    chats.ChatRepo,
    sheets.SheetsRepo,
    workers.WorkerRepo,
):
    """
    DbClient class to manage some repo related tasks
    """
