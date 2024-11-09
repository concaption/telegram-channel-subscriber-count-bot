"""
- This module is responsible for providing the method to delete worker from the database
"""
from sqlalchemy.orm import Session

from .. import workers


class DeleteWorker:
    """
    Provides the methods to delete worker from the database
    """
    @classmethod
    def delete_worker(
        cls: "workers.WorkerRepo", session: Session
    ) -> None:
        """
        Returns the worker from the database
        :param session:
        :return:
        """
        worker = cls.get_worker(session)
        if worker is not None:
            session.delete(worker)
