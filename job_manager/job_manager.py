"""
- This module is responsible for handling the task of sending scheduled messages
"""
import datetime
from typing import Union

from apscheduler.job import Job
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from pyrogram.enums import ChatType

from bot import BotManager
from gsheet import Gsheet
from database import DbClient, DbHelper


class JobManager:
    """
    Responsible for managing the jobs
    """
    _scheduler = AsyncIOScheduler()
    job: Union[Job, None] = None

    @staticmethod
    async def the_job() -> None:
        """
        The job of sending the scheduled messages
        :return:
        """
        client = BotManager.get_worker()
        now = datetime.datetime.utcnow()
        with DbHelper.session_manager() as session:
            db_sheet = DbClient.get_sheet(session)
            if db_sheet is not None:
                if client is not None and Gsheet.service_email is not None:
                    async for dialog in client.get_dialogs():
                        chat = dialog.chat
                        if chat.type in {ChatType.GROUP, ChatType.SUPERGROUP, ChatType.CHANNEL}:
                            data = [chat.title, str(chat.id), str(chat.members_count), now.strftime("%d/%m/%Y %I:%M %p")]
                            try:
                                Gsheet.add_data(
                                    sheet_url=db_sheet.url,
                                    values=data,
                                )

                            except Exception as e:
                                print(f"Error occurred while adding data: {str(e)}")
                                pass

    @classmethod
    def refresh_jobs(cls) -> None:
        """
        Refreshes the job
        :return:
        """
        trigger = CronTrigger(
            hour=0,
            minute=1,
        )
        job = cls._scheduler.add_job(
            func=cls.the_job,
            trigger=trigger,
        )
        cls.job = job
        cls._scheduler.start()
