"""
- This module is responsible for handling the start command
"""
import datetime

from pyrogram.enums import ChatType
from pyrogram.types import Message
from sqlalchemy.orm import Session

from .utils import Utils
from bot import BotManager
from database import DbClient
from gsheet import Gsheet
from job_manager import JobManager


async def handle_start_command(update: Message, session: Session) -> None:
    """
    Handles the start command
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
                commands = ("#COMMANDS:\n"
                            "/auth -> to authorize a google service account\n"
                            "/sheet -> to connect a google sheet\n"
                            "/worker -> to connect a worker")
                service_email = Gsheet.service_email
                service_email_text = f"Service Email: {service_email}"
                if not service_email:
                    service_email_text = ("Please authorize a google service account using the /auth "
                                          "command.")
                client = BotManager.get_worker()
                if client is not None:
                    client_text = f"Worker: {client.phone_number}"

                else:
                    client_text = "Please connect a worker using the /worker command"
                db_sheet = DbClient.get_sheet(session)
                if db_sheet is not None:
                    sheet_text = f"Sheet: {db_sheet.url}"

                else:
                    sheet_text = "Please connect a google sheet using the /sheet command"

                job = JobManager.job
                if job is not None:
                    next_run_time: datetime.datetime = job.next_run_time
                    job_next_run_time = f"Next Task: {next_run_time.strftime('%d/%m/%Y %I:%M %p')}"

                else:
                    job_next_run_time = ""

                text = (f"{service_email_text}\n\n"
                        f"{client_text}\n\n"
                        f"{sheet_text}\n\n"
                        f"{job_next_run_time}\n\n\n"
                        f"{commands}")

    if text:
        await update.reply_text(
            text=text,
        )
