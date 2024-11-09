"""
- This module is responsible for defining the methods to get the chats from the database
"""
from typing import Union

from pyrogram import types
from sqlalchemy.orm import Session

from ... import models


chat_type = "models.chats.Chat"


class GetChat:
    """
    Provides the method to get chats from the database
    """
    @staticmethod
    def get_chat_via_chat_id(chat_id: int, session: Session) -> Union[chat_type, None]:
        """
        Returns the chat from the database using the telegram id of the chat
        """
        chat_cls = models.chats.Chat
        db_chat = session.query(chat_cls).filter(chat_cls.chat_id == chat_id).one_or_none()
        return db_chat

    @classmethod
    def get_chat(cls, tg_chat: types.Chat, session: Session) -> Union[chat_type, None]:
        """
        Returns the chat from the database using the telegram's chat object
        """
        return cls.get_chat_via_chat_id(chat_id=tg_chat.id, session=session)
