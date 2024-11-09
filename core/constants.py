"""
- This module defines some constants
For FUN :)
"""
import logging
from pathlib import Path


log = logging.getLogger(__name__)


class Constant:
    """
    Class to hold the constant variables
    """
    one_minute = 60
    data_dir = Path.cwd().joinpath(".data")
    db_path = f"sqlite:///{data_dir}/database.db"
    debug = True

    @classmethod
    def create_data_dir(cls) -> None:
        """
        Creates the data directory
        :return:
        """
        log.info("creating data directory with path: %s", cls.data_dir)
        cls.data_dir.mkdir(exist_ok=True)


# creates the data directory
Constant.create_data_dir()
