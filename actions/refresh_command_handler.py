"""
- This module is responsible for handling the /refresh command
"""
from pyrogram.enums import ChatType
from pyrogram.types import Message
from sqlalchemy.orm import Session

from .utils import Utils
from database import DbClient
from job_manager import JobManager


async def handle_refresh_command(update: Message, session: Session) -> None:
    """
    Handles the refresh command
    :param update:
    :param session:
    :return:
    """
    text = None
    await Utils.create_chat(update=update, session=session)
    tg_chat = update.chat
    if tg_chat.type != ChatType.PRIVATE:
        db_admin_chat = DbClient.get_admin_chat(session)
        if db_admin_chat is not None:
            if tg_chat.id == db_admin_chat.chat_id:
                await update.reply_text(
                    text="Okay, manually triggering the job. You'll be notified once it's done",
                )
                await JobManager.the_job()
                text = "Successfully completed the job."

    if text:
        await update.reply_text(
            text=text,
        )
