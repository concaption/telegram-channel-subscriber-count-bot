"""
- This script is responsible for handling text messages
"""
import re
from typing import Optional

from pyrogram.enums import ChatType
from pyrogram.types import Message
from pyrogram.errors.exceptions import BadRequest, SessionPasswordNeeded, PhoneNumberInvalid
from sqlalchemy.orm import Session

from bot import BotManager
from config import ConfigRepo
from database import DbClient
from state_manager import States, StateManager

temp_phone_number: Optional[str] = None
error_count = 0


async def handle_text_message(update: Message, session: Session) -> None:
    """
    Handles the text messages received by the bot
    :param update:
    :param session:
    :return:
    """
    global error_count, temp_phone_number
    text = None
    send_a_valid_phone_number = "Please send a valid phone number in international format. Eg: +12324455678"
    max_try_exceeded = "Max try exceeded. Please try again later."
    if update.chat.type in {ChatType.GROUP, ChatType.SUPERGROUP}:
        DbClient.add_chat(tg_chat=update.chat, session=session)
        admin_chat = DbClient.get_admin_chat(session)
        if admin_chat is not None:
            tg_chat = update.chat
            msg_text = update.text
            if admin_chat.chat_id != tg_chat.id:
                return

            # if the message doesn't contain any text
            if not msg_text:
                return

            current_state = StateManager.get_state(chat_id=tg_chat.id)
            #  if we don't have any special state, ignore
            if current_state == States.start:
                return

            # if we are expecting phone number from the user
            elif current_state == States.phone_number:
                phone_number = msg_text
                if not phone_number.startswith("+"):
                    text = send_a_valid_phone_number
                    error_count += 1

                elif 10 > len(phone_number) > 14:
                    text = send_a_valid_phone_number
                    error_count += 1

                else:
                    if BotManager.temp_client:
                        try:
                            await BotManager.temp_client.disconnect()

                        except ConnectionError:
                            pass

                    temp_phone_number = phone_number
                    config = ConfigRepo.get_config()
                    try:
                        client = BotManager.get_temp_client(
                            api_id=config.api_id,
                            api_hash=config.api_hash,
                            phone_number=phone_number,
                        )
                        await client.connect()
                        BotManager.temp_client = client
                        sent_code = await client.send_code(
                            phone_number=phone_number,
                        )
                        BotManager.temp_sent_code = sent_code

                    except (BadRequest, PhoneNumberInvalid):
                        text = ("Telegram is not allowing logging into this account at the moment. Maybe try after "
                                "some time!")
                        StateManager.update_state(chat_id=tg_chat.id, state=States.start)
                        error_count = 0

                    else:
                        text = (f"Log in code sent!\n"
                                f"Please send the login code like HELLO`<login_code>`. Eg: if the code you received "
                                f"is 12345, then send a message like HELLO12345.")
                        StateManager.update_state(chat_id=tg_chat.id, state=States.otp)
                        error_count = 0

            # if we are expecting otp from the user
            elif current_state == States.otp:
                login_code = re.search(pattern=r"\d+", string=msg_text).group()
                if login_code:
                    try:
                        await BotManager.temp_client.sign_in(
                            phone_number=temp_phone_number,
                            phone_code_hash=BotManager.temp_sent_code.phone_code_hash,
                            phone_code=login_code,
                        )
                    
                    except SessionPasswordNeeded:
                        text = f"Please enter the 2fa password of the worker account: {temp_phone_number}"
                        error_count = 0
                        StateManager.update_state(chat_id=tg_chat.id, state=States.two_fa)

                    except BadRequest:
                        text = f"Log in code invalid or expired. Please send a valid login code."
                        error_count += 1
                    
                    else:
                        text = f"Successfully added worker: {temp_phone_number}"
                        DbClient.add_worker(
                            phone_number=temp_phone_number,
                            session=session,
                        )
                        BotManager.worker = BotManager.temp_client
                        BotManager.temp_client = None
                        BotManager.temp_sent_code = None
                        StateManager.update_state(chat_id=update.chat.id, state=States.start)

                else:
                    text = (f"Expecting the log in code to log into the worker: {temp_phone_number}.\n"
                            f"To cancel the operation send /start")
                    
            elif current_state == States.two_fa:
                try:
                    await BotManager.temp_client.check_password(
                        password=msg_text,
                    )
                
                except BadRequest:
                    text = "Incorrect 2FA password entered. Please enter a valid 2FA password."
                    error_count += 1
                
                else:
                    text = f"Successfully added worker: {temp_phone_number}"
                    DbClient.add_worker(
                        phone_number=temp_phone_number,
                        session=session,
                    )
                    BotManager.worker = BotManager.temp_client
                    BotManager.temp_client = None
                    BotManager.temp_sent_code = None
                    StateManager.update_state(chat_id=update.chat.id, state=States.start)

    if error_count > 3:
        text = max_try_exceeded
        StateManager.update_state(chat_id=update.chat.id, state=States.start)
        error_count = 0
        try:
            if BotManager.temp_client:
                await BotManager.temp_client.disconnect()
        
        except ConnectionError:
            pass

    if text:
        await update.reply_text(
            text=text,
        )
