"""
- This module is responsible for creating and providing app wide configurations
"""
import logging
import os
from typing import Union

from config import Config


log = logging.getLogger(__name__)


class ConfigRepo:
    """
    ConfigRepo class provide create and provide app wide configurations
    """
    _instance: Union[Config, None] = None

    @classmethod
    def _get_config(cls) -> Config:
        """
        Returns the configuration from the env
        :return:
        """
        log.info("getting config from environment")
        # Telegram api related
        api_id = os.getenv("API_ID")
        log.info("api_id: %s", api_id)
        api_hash = os.getenv("API_HASH")
        log.info("api_hash: %s", api_hash)
        bot_token = os.getenv("BOT_TOKEN")
        log.info("bot_token: %s", bot_token)

        data = {
            "api_id": api_id,
            "api_hash": api_hash,
            "bot_token": bot_token,
        }

        log.info("config data: %s", str(data))
        config = Config(
            **data,
        )

        return config

    @classmethod
    def get_config(cls) -> Config:
        """
        Returns the config that has been loaded
        :return:
        """
        log.info("called class get config")
        if cls._instance is None:
            cls._instance = cls._get_config()

        return cls._instance
