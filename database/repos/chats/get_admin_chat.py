"""
- This module is responsible for providing the method to get the admin chat from the database
"""
from typing import Union

from sqlalchemy.orm import Session

from ... import models


class GetAdminChat:
    """
    Provides the methods to get the admin chat from the database
    """
    @staticmethod
    def get_admin_chat(session: Session) -> Union["models.chats.Chat", None]:
        """
        Returns the admin chat from the database if exits, else None
        :param session:
        :return:
        """
        chat_cls = models.chats.Chat
        db_chat = session.query(
            chat_cls
        ).filter(
            chat_cls.is_admin_chat.is_(True)
        ).one_or_none()
        return db_chat
