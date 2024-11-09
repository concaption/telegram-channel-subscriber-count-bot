"""
- This module defines the configurations needed for the application
"""
from pydantic import BaseModel


class Config(BaseModel):
    """
    Config class to manage app-wide configurations
    """
    # telegram api id
    api_id: int
    # telegram api hash
    api_hash: str
    # telegram bot token
    bot_token: str
