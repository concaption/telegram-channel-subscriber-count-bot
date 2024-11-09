"""
- This module is responsible for managing the bots
"""
import logging
from pathlib import Path
from typing import Union

from pyrogram import Client, idle
from pyrogram.types import User, SentCode

from core import Constant


log = logging.getLogger(__name__)


class BotManager:
    """
    BotManager class to manage the bots
    """
    _main_bot: Union[Client, None] = None
    worker: Union[Client, None] = None
    _is_idle: bool = False
    main_client_info: Union[User, None] = None
    temp_client: Union[Client, None] = None
    temp_sent_code: Union[SentCode, None] = None

    @staticmethod
    def get_temp_client(
        api_id: int,
        api_hash: str,
        phone_number: str,
        sleep_threshold: int = 3 * Constant.one_minute,
    ) -> Client:
        """
        Returns the temp client
        :return:
        """
        session_name = phone_number.replace("+", "")
        client = Client(
            name=session_name,
            api_id=api_id,
            api_hash=api_hash,
            phone_number=phone_number,
            sleep_threshold=sleep_threshold,
            workdir=str(Constant.data_dir),
            no_updates=True,
        )
        return client

    @classmethod
    async def start_bot(
        cls,
        api_id: int,
        api_hash: str,
        bot_token: str,
        session_name: str,
        work_dir: Path,
        sleep_threshold: int = 3 * Constant.one_minute,
    ) -> Client:
        """
        Starts the telegram bot and keeps it running
        :param api_id:
        :param api_hash:
        :param bot_token:
        :param session_name:
        :param work_dir:
        :param sleep_threshold: int = 3 * Constant.one_minute,
        :return:
        """
        log.info("starting bot with api_id: %s, api_hash: %s, bot_token: %s, session_name: %s",
                 api_id, api_hash, bot_token, session_name)
        client = Client(
            name=session_name,
            api_id=api_id,
            api_hash=api_hash,
            bot_token=bot_token,
            sleep_threshold=sleep_threshold,
            plugins={"root": "handlers"},
            workdir=str(work_dir),
        )
        await client.start()
        me = await client.get_me()
        cls.main_client_info = me
        log.info("bot started: @%s", me.username)
        cls._main_bot = client
        print(f"bot started: @{me.username}")
        return client

    @classmethod
    async def start_worker(
        cls,
        api_id: int,
        api_hash: str,
        phone_number: str,
    ) -> Client:
        """
        Starts the worker
        :param api_id:
        :param api_hash:
        :param phone_number:
        :return:
        """
        log.info("starting the worker with api_id: %s, api_hash: %s, phone_number: %s, ",
                 api_id, api_hash, phone_number,)
        client = cls.get_temp_client(
            api_id=api_id,
            api_hash=api_hash,
            phone_number=phone_number,
        )
        cls.worker = await client.start()
        me = await client.get_me()
        log.info("worker started: %s", me.phone_number)
        print(f"worker started: {me.phone_number}")
        return client

    @classmethod
    def get_bot(cls) -> Union[Client, None]:
        """
        Returns the telegram client if it's running
        :return:
        """
        return cls._main_bot

    @classmethod
    def get_worker(cls) -> Union[Client, None]:
        """
        Returns the worker if exists
        :return:
        """
        return cls.worker

    @classmethod
    async def stop_bot(cls) -> None:
        """
        Stops the bot if it exists
        :return:
        """
        client = cls._main_bot
        if client is not None:
            await client.stop()

    @classmethod
    async def stop_worker(cls) -> None:
        """
        Stops the worker
        :return:
        """
        if cls.worker:
            try:
                await cls.worker.stop()

            except ConnectionError:
                pass

            cls.worker = None

    @classmethod
    async def keep_running(cls) -> None:
        """
        Keeps running the bot forever
        """
        log.info("calling keep running method to idle the bots")
        if not cls._is_idle:
            log.debug("calling the idle method of pyrogram")
            cls._is_idle = True
            await idle()
