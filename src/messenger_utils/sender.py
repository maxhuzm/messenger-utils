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

    def __init__(self, api_url: str, secret_key: str):
        """
        Constructor.
        
        :param api_url: URL of the messenger's API endpoint.
        :param secret_key: Secret key for API authentication.
        """
        self.api_url = api_url
        self.secret_key = secret_key



    @abstractmethod
    def send_text_message(self, message: str):
        """
        Sends a message to the messenger's webhook URL.
        
        :param message: text message to send
        :kwargs: other arguments to declare in derived classes
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