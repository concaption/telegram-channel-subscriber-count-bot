"""
- This module is responsible for handling the /auth command
"""
import json

from pyrogram.enums import ChatType
from pyrogram.types import Message
from sqlalchemy.orm import Session

from .utils import Utils
from database import DbClient
from gsheet import Gsheet


async def handle_auth_command(update: Message, session: Session) -> None:
    """
    Handles the auth command
    :param update:
    :param session:
    :return:
    """
    text = None
    command_guide = ("To authorize a google service account, send the json key of the service account, and in "
                     "reply to that json file, send /auth.")
    await Utils.create_chat(update=update, session=session)
    tg_chat = update.chat
    if tg_chat.type != ChatType.PRIVATE:
        db_admin_chat = DbClient.get_admin_chat(session)
        if db_admin_chat is not None:
            if tg_chat.id == db_admin_chat.chat_id:
                command = update.command
                if len(command) == 1:
                    replied_message = update.reply_to_message
                    if not replied_message:
                        text = "Please send this command in reply to the json file."

                    else:
                        document = replied_message.document
                        if not document:
                            text = "Please send this command in reply to the json file."

                        else:
                            if not document.file_name.endswith("json"):
                                text = "Please send this command in reply to the json file."

                            else:
                                json_file = await replied_message.download()
                                with open(json_file, "r") as f:
                                    try:
                                        json_data = json.load(f)

                                    except json.JSONDecodeError:
                                        text = "Invalid key file provided."

                                    else:
                                        Gsheet.authorize(key_data=json_data)
                                        text = f"Okay, the bot is now using the service account: {Gsheet.service_email}"

                else:
                    text = command_guide

    if text:
        await update.reply_text(
            text=text,
        )
