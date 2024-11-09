"""
- This module is responsible for providing the methods related to the workers
"""
from .add_worker import AddWorker
from .delete_worker import DeleteWorker
from .get_worker import GetWorker


class WorkerRepo(
    AddWorker,
    DeleteWorker,
    GetWorker,
):
    """
    Provides the methods related to workers
    """
