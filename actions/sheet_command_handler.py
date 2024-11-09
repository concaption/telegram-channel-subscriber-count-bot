"""
- This module is responsible for handling the /sheet command
"""
from pyrogram.enums import ChatType
from pyrogram.types import Message
from sqlalchemy.orm import Session

from .utils import Utils
from database import DbClient
from gsheet import Gsheet


async def handle_sheet_command(update: Message, session: Session) -> None:
    """
    Handles the sheet command
    :param update:
    :param session:
    :return:
    """
    text = None
    command_guide = "To connect a google sheet, send the command like this, /sheet `sheet_url`"
    await Utils.create_chat(update=update, session=session)
    tg_chat = update.chat
    if tg_chat.type != ChatType.PRIVATE:
        db_admin_chat = DbClient.get_admin_chat(session)
        if db_admin_chat is not None:
            if tg_chat.id == db_admin_chat.chat_id:
                command = update.command
                if len(command) == 2:
                    link = command[-1]
                    if not Gsheet.service_email:
                        text = ("Gsheet service account is not authorized please use the /auth command to authorize "
                                "a service account.")

                    else:
                        if link.startswith("https://docs.google.com"):
                            error = Gsheet.has_access(sheet_url=link)
                            if error:
                                text = error

                            else:
                                DbClient.add_sheet(
                                    sheet_url=link,
                                    session=session,
                                )
                                text = "Okay, google sheet updated, bot will post the data on this sheet from now on."

                        else:
                            text = "Invalid link provided please provide a valid link."

                else:
                    text = command_guide

    if text:
        await update.reply_text(
            text=text,
        )
