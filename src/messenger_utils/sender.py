"""
Message send functionality for messenger_utils
"""

import httpx
from abc import ABC, abstractmethod


### CLASS `Sender` ###

class Sender(ABC):
    """
    Sender abstract class to send messages to messenger via API.
    Particular functionality is implemented in derived classes.
    """

    def __init__(self, bot_token: str):
        """
        Init Sender object.
        
        :param secret_key: Secret key for API authentication.
        """
        self.bot_token = bot_token



    @abstractmethod
    async def send_text_message(self, text: str, target: str):
        """
        Sends a message to the messenger's webhook URL.
        
        :param message: text message to send
        :param target: user_id, chat_id, etc. (see docs in derived classes)
        """
        pass



### END OF CLASS `SENDER`` ###