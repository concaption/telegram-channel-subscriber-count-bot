"""
- This module is responsible for providing the methods to add chats to the database
"""
from pyrogram import types
from sqlalchemy.orm import Session

from .. import chats
from ... import models


class AddChat:
    """
    Provides the method to add chats to the database
    """
    @classmethod
    def add_chat(cls: "chats.ChatRepo", tg_chat: types.Chat, session: Session) -> "models.chats.Chat":
        """
        Adds details about a telegram chat in the database
        """
        chat_cls = models.chats.Chat
        db_chat = cls.get_chat(tg_chat=tg_chat, session=session)
        if db_chat is None:
            db_chat = chat_cls(
                chat_id=tg_chat.id,
                title=tg_chat.title,
            )
            session.add(db_chat)

        return db_chat
