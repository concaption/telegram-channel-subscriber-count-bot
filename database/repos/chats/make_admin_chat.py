"""
- This module is responsible for providing the method to mark a chat as admin
"""
from typing import Union

from sqlalchemy.orm import Session

from .. import chats
# from ... import models


chat_type = "models.chats.Chat"


class MakeAdminChat:
    """
    Provides the methods to make a chat admin chat
    """
    @classmethod
    def make_admin_chat(
        cls: "chats.ChatRepo",
        db_chat: chat_type,
        session: Session
    ) -> Union[chat_type, None]:
        """
        Returns the admin chat from the database if exits, else None
        :param db_chat:
        :param session:
        :return:
        """
        db_admin_chat = cls.get_admin_chat(session=session)
        if db_admin_chat is None:
            db_chat.is_admin_chat = True

        return db_chat

