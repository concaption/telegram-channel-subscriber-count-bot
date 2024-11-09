"""
- This module is responsible for handling the /worker command
"""
from pyrogram.enums import ChatType
from pyrogram.types import Message
from sqlalchemy.orm import Session

from bot import BotManager
from database import DbClient
from state_manager import States, StateManager


async def handle_worker_command(update: Message, session: Session) -> None:
    """
    Handles the worker command
    :param update:
    :param session:
    :return:
    """
    text = None
    command_guide = ("Send /worker -> to view details of the current worker\n"
                     "Send /worker add -> to add new worker\n"
                     "Send /worker remove -> to remove the worker.")
    if update.chat.type in {ChatType.GROUP, ChatType.SUPERGROUP}:
        DbClient.add_chat(tg_chat=update.chat, session=session)
        admin_chat = DbClient.get_admin_chat(session)
        if admin_chat is not None:
            if update.chat.id != admin_chat.chat_id:
                return

            command = update.command
            if len(command) == 1:
                db_worker = DbClient.get_worker(session)
                if db_worker is None:
                    text = "No worker is added! Please add worker using the /worker add command."

                else:
                    text = (f"Current worker: `{db_worker.phone_number}`\n"
                            f"To remove the worker send /worker remove")

            elif len(command) == 2:
                db_worker = DbClient.get_worker(session)
                if command[1].lower() == "add":
                    if db_worker is None:
                        text = ("Please send the phone number of the account that you want to add as worker! "
                                "Make sure, you are already logged into this telegram account.")
                        StateManager.update_state(chat_id=update.chat.id, state=States.phone_number)

                    else:
                        text = (f"{db_worker.phone_number} is already added as worker, please remove the worker "
                                f"before adding new worker!")

                elif command[1].lower() == "remove":
                    if db_worker is None:
                        text = "No worker is currently added. You can add using the /worker add command."

                    else:
                        await BotManager.stop_worker()
                        DbClient.delete_worker(session)
                        text = "Worker removed! You can add worker using /worker add"

                else:
                    text = command_guide

            else:
                text = command_guide

    if text:
        await update.reply_text(
            text=text,
        )
