"""
- Responsible for providing some utility functions
"""
import logging
from typing import Union

from pyrogram import Client
from pyrogram.enums import ChatType
from pyrogram.types import Message, User
from pyrogram.raw.functions.channels import CreateForumTopic
from pyrogram.raw.functions.messages import ForwardMessages
from pyrogram.raw.types import MessageActionTopicCreate, MessageService, Updates, UpdateNewChannelMessage
from sqlalchemy.orm import Session

from database import DbClient


log = logging.getLogger(__name__)


class Utils:
    """
    Provides utility methods
    """
    @staticmethod
    def _get_formatted_chat_id(chat_id: str) -> str:
        """
        Returns the chat id after formatting
        :param chat_id:
        :return:
        """
        formatted_chat_id = chat_id.replace("-100", "").replace("-", "")
        return formatted_chat_id

    @classmethod
    def get_chat_link(cls, chat_id: Union[int, str]) -> str:
        """
        Returns the link that opens the chat using the id of the chat
        :param chat_id:
        :return:
        """
        chat_id = str(chat_id)
        formatted_chat_id = cls._get_formatted_chat_id(chat_id=chat_id)
        link = f"https://t.me/c/{formatted_chat_id}"
        return link

    @classmethod
    def get_msg_link(cls, chat_id: int, msg_id: int) -> str:
        """
        Returns the link that points to this file
        :param chat_id:
        :param msg_id:
        :return:
        """
        chat_id = str(chat_id)
        formatted_chat_id = cls._get_formatted_chat_id(chat_id=chat_id)
        link = f"https://t.me/c/{formatted_chat_id}/{msg_id}"
        return link

    @staticmethod
    async def create_topic(
        client: Client,
        update: Message,
        chat_id: int,
        topic_title: str = None,
    ) -> int:
        """
        Creates the topic and returns the id of the topic
        :param client:
        :param update:
        :param chat_id:
        :param topic_title:
        :return:
        """
        log.info("calling method create_topic")
        tg_user = update.from_user
        topic_title = topic_title or f"{tg_user.first_name} #{tg_user.id}"
        input_peer = await client.resolve_peer(peer_id=chat_id)
        updates: Updates = await client.invoke(
            CreateForumTopic(
                channel=input_peer,
                title=topic_title,
                random_id=update.id,
            )
        )

        for update in updates.updates:
            if isinstance(update, UpdateNewChannelMessage):
                if isinstance(update.message, MessageService):
                    if isinstance(update.message.action, MessageActionTopicCreate):
                        topic_id = update.message.id
                        return topic_id

    @staticmethod
    async def get_user_dp(
        client: Client,
        tg_user: User,
    ) -> Union[str, None]:
        """
        Returns the file id of the profile picture, if exists else None
        :param client:
        :param tg_user:
        :return:
        """
        photo = None
        photos_count = await client.get_chat_photos_count(chat_id=tg_user.id)
        if photos_count > 0:
            async for c_photo in client.get_chat_photos(chat_id=tg_user.id, limit=1):
                photo = c_photo.file_id
                break

        return photo

    @staticmethod
    async def send_support_request(
        client: Client,
        admin_chat_id: int,
        topic_id: int,
    ) -> None:
        """
        Sends a support request in the admin chat
        :param client:
        :param admin_chat_id:
        :param topic_id:
        :return:
        """
        if admin_chat_id is not None:
            await client.send_message(
                chat_id=admin_chat_id,
                reply_to_message_id=topic_id,
                text="#SUPPORT\n\n"
                     "The user is asking for support request, send /support to provide support!",
            )

    @staticmethod
    async def forward_user_message(
        client: Client,
        admin_chat_id: int,
        topic_id: int,
        user_id: int,
        msg_id: int,
    ) -> None:
        """
        Forwards the message of the user to the admin chat topic
        :param client:
        :param admin_chat_id:
        :param topic_id:
        :param user_id:
        :param msg_id:
        :return:
        """
        if admin_chat_id is not None:
            await client.invoke(
                ForwardMessages(
                    from_peer=await client.resolve_peer(user_id),
                    to_peer=await client.resolve_peer(admin_chat_id),
                    id=[msg_id],
                    random_id=[msg_id],
                    top_msg_id=topic_id,
                )
            )

    @classmethod
    async def send_new_user_info(
        cls,
        client: Client,
        update: Message,
        admin_chat_id: int,
        topic_id: int,
    ) -> None:
        """
        Sends info about the new user in the admin chat
        :return:
        """
        tg_user = update.from_user
        log.info(
            "sending new user info about user: %s , on admin_chat_id: %s, topic_id: %s, ",
            tg_user, admin_chat_id, topic_id
        )

        response_text = f"""
#NEWUSER 
ID: {tg_user.id}
Name: {tg_user.first_name} {tg_user.last_name if tg_user.last_name else ""}
Username: {f'@{tg_user.username}' if tg_user.username is not None else 'Not Available'}
"""
        photo = await cls.get_user_dp(client=client, tg_user=tg_user)
        # if the user doesn't have a chat photo
        if photo is None:
            await client.send_message(
                chat_id=admin_chat_id,
                text=response_text,
                reply_to_message_id=topic_id,
            )

        else:
            await client.send_cached_media(
                chat_id=admin_chat_id,
                file_id=photo,
                caption=response_text,
                reply_to_message_id=topic_id,
            )

    @staticmethod
    async def create_chat(update: Message, session: Session) -> None:
        """
        Creates a chat in the database
        """
        tg_chat = update.chat
        if tg_chat.type != ChatType.PRIVATE:
            DbClient.add_chat(
                tg_chat=tg_chat,
                session=session,
            )
