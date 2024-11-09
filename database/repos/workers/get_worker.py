"""
- This module is responsible for getting the worker from the database
"""
from typing import Union

from sqlalchemy.orm import Session

from ... import models


class GetWorker:
    """
    Provides the methods to get the worker from the database
    """
    @staticmethod
    def get_worker(session: Session) -> Union["models.workers.Worker", None]:
        """
        Returns the worker from the database
        :param session:
        :return:
        """
        worker_cls = models.workers.Worker
        worker = session.query(worker_cls).first()
        return worker
