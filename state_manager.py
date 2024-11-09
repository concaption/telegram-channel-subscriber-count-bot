"""
- This module is responsible for managing the state of the program
"""
from enum import Enum
from typing import Dict


class States(Enum):
    start = "start"
    phone_number = "phone_number"
    otp = "otp"
    two_fa = "two_fa"


class StateManager:
    """
    Responsible for managing the state
    """
    _default_state = States.start
    _states: Dict[int, States] = dict()

    @classmethod
    def get_state(cls, chat_id: int) -> States:
        """
        Returns the state of the chat
        :param chat_id:
        :return:
        """
        state = cls._states.get(chat_id)
        if state is None:
            state = States.start

        return state

    @classmethod
    def update_state(cls, chat_id: int, state: States) -> None:
        """
        Updates the state of the chat
        :param chat_id:
        :param state:
        :return:
        """
        cls._states[chat_id] = state
