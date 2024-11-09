"""
- This module is responsible for representing a telegram chat in the database
"""
from sqlalchemy import Boolean, Column, Integer, String

from ..base import Base
from ..tables import Tables


class Chat(Base):
    """
    Represents a telegram chat in the database
    """
    # name of the database table is `chats`
    __tablename__ = Tables.chats

    # auto generated primary key of the chat
    id = Column(Integer, primary_key=True, autoincrement=True)
    # telegram id of the chat
    chat_id = Column(Integer, index=True)
    # why don't use the chat id as the primary key?
    # because telegram might change that :)
    # title of the chat
    title = Column(String, nullable=False)
    # whether the chat is the admin chat or not
    is_admin_chat = Column(Boolean, default=False)

    def __init__(
        self,
        chat_id: int,
        title: str
    ):
        self.chat_id = chat_id
        self.title = title
