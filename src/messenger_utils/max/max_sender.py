"""
Sender functionality for MAX messenger.

Contains class MaxSender, derived from Sender abstract class.
"""

import httpx
from messenger_utils.sender import Sender


###   Class MaxSender   ###

class MaxSender(Sender):
    """
    Sender class for MAX messenger.
    
    Derived from Sender abstract class.
    """

    def __init__(self, api_url: str, secret_key: str):
        """
        Constructor.
        
        :param api_url: URL of the messenger's API endpoint.
        :param secret_key: Secret key for API authentication.
        """
        super().__init__(api_url, secret_key)



    def send_text_message(self, message: str):
        """
        Send text message to the MAX user / chat via API.
        
        :param message: text message to send
        """
        pass



    def send_keyboard_message(self, message: str, keyboard: list[list[str]]):
        """
        Send message with inline keyboard to the MAX user / chat via API.
        
        :param message: text message to send
        :keyboard: 2d-array of buttons       
        """
        pass



    def declare_bot_command(self, *, command: str, description: str):
        """
        Declare command (starting with /) for the MAX Bot
        
        :param command: command to declare
        :param description: description of the command
        """
        pass


###   End of class MaxSender   ###