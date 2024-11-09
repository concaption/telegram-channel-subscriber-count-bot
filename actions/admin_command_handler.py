"""
- This module is responsible for handling the /admin command
"""
from pyrogram.enums import ChatType
from pyrogram.types import Message
from sqlalchemy.orm import Session

from .utils import Utils
from database import DbClient


async def handle_admin_command(update: Message, session: Session) -> None:
    """
    Handles the admin command
    :param update:
    :param session:
    :return:
    """
    text = None
    await Utils.create_chat(update=update, session=session)
    tg_chat = update.chat
    if tg_chat.type != ChatType.PRIVATE:
        db_admin_chat = DbClient.get_admin_chat(session)
        if db_admin_chat is None:
            db_chat = DbClient.get_chat(tg_chat=tg_chat, session=session)
            DbClient.make_admin_chat(db_chat=db_chat, session=session)
            text = "Okay, this chat has been marked as the admin chat."

        else:
            if tg_chat.id == db_admin_chat.chat_id:
                text = "Don't worry, this chat is already marked as the admin chat."

    if text:
        await update.reply_text(
            text=text,
        )
