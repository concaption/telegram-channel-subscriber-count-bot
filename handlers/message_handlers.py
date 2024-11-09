"""
- This module is responsible for handling the messages received by the bot
"""
from pyrogram import Client, filters
from pyrogram.types import Message

from actions import (
    handle_admin_command,
    handle_auth_command,
    handle_refresh_command,
    handle_sheet_command,
    handle_start_command,
    handle_text_message,
    handle_worker_command,
)
from database import DbHelper


@Client.on_message(filters.command("start"))
async def start_command_handler(_: Client, update: Message) -> None:
    """
    Responsible for handling the /start command
    """
    with DbHelper.session_manager() as session:
        await handle_start_command(update=update, session=session)


@Client.on_message(filters.command("admin"))
async def admin_command_handler(_: Client, update: Message) -> None:
    """
    Responsible for handling the /admin command
    """
    with DbHelper.session_manager() as session:
        await handle_admin_command(update=update, session=session)


@Client.on_message(filters.command("sheet"))
async def sheet_command_handler(_: Client, update: Message) -> None:
    """
    Responsible for handling the /sheet command
    """
    with DbHelper.session_manager() as session:
        await handle_sheet_command(update=update, session=session)


@Client.on_message(filters.command("auth"))
async def auth_command_handler(_: Client, update: Message) -> None:
    """
    Responsible for handling the /auth command
    """
    with DbHelper.session_manager() as session:
        await handle_auth_command(update=update, session=session)


@Client.on_message(filters.command("worker"))
async def worker_command_handler(_: Client, update: Message) -> None:
    """
    Responsible for handling the /worker command
    """
    with DbHelper.session_manager() as session:
        await handle_worker_command(update=update, session=session)


@Client.on_message(filters.command("refresh"))
async def refresh_command_handler(_: Client, update: Message) -> None:
    """
    Responsible for handling the /worker command
    """
    with DbHelper.session_manager() as session:
        await handle_refresh_command(update=update, session=session)


@Client.on_message(filters.text)
async def text_messages_handler(_: Client, update: Message) -> None:
    """
    Responsible for handling all the text messages
    """
    with DbHelper.session_manager() as session:
        await handle_text_message(update=update, session=session)
