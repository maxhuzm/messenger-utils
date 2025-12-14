"""
Message send functionality for messenger_utils

"""

import httpx
from abc import ABC, abstractmethod


### CLASS `SENDER` ###

class Sender(ABC):
    """
    Sender abstract class to send messages to messenger via API.
    Particular functionality is implemented in derived classes.
    """

    def __init__(self, bot_token: str):
        """
        Constructor.
        
        :param api_url: URL of the messenger's API endpoint.
        :param secret_key: Secret key for API authentication.
        """
        self.bot_token = bot_token



    @abstractmethod
    async def send_text_message(self, message: str, target: str):
        """
        Sends a message to the messenger's webhook URL.
        
        :param message: text message to send
        :param target: user_id, chat_id, etc. (see docs in derived classes)
        """
        pass



    @abstractmethod
    def declare_bot_command(self, *, command: str, description: str):
        """
        Declare command (starting with /) for the Bot
        
        :param command: command to declare
        :param description: description of the command
        """
        pass


### END OF CLASS `SENDER`` ###