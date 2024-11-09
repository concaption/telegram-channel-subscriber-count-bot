"""
- This module is responsible for providing the methods needed to interact with the database chats
"""
from .add_chat import AddChat
from .get_admin_chat import GetAdminChat
from .get_chat import GetChat
from .make_admin_chat import MakeAdminChat


class ChatRepo(
    AddChat,
    GetAdminChat,
    GetChat,
    MakeAdminChat,
):
    """
    Provides the methods related to chats
    """
