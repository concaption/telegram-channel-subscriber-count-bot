"""
- This module is responsible for handling the task of adding worker
"""
from typing import Union

from sqlalchemy.orm import Session

from .. import workers
from ... import models


class AddWorker:
    """
    Provides the methods to add workers in the database
    """
    @classmethod
    def add_worker(
        cls: "workers.WorkerRepo", phone_number: str, session: Session
    ) -> Union["models.workers.Worker", None]:
        """
        Responsible for adding worker in the database
        :param phone_number:
        :param session:
        :return:
        """
        worker_cls = models.workers.Worker
        worker = cls.get_worker(session)
        if worker is None:
            worker = worker_cls(
                phone_number=phone_number,
            )
            session.add(worker)

        return worker
