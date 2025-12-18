"""
Sender functionality for MAX messenger.

Contains class MaxSender, derived from Sender abstract class.
"""

import json
import httpx
from messenger_utils.sender import Sender
from messenger_utils.max.max_keyboard import *
from . import MAX_API_URL


###   Class MaxSender   ###

class MaxSender(Sender):
    """
    Sender class for MAX messenger.
    
    Derived from Sender abstract class.
    """

    def __init__(
        self,
        bot_token: str
    ):
        """
        Constructor.
        
        :param secret_key: Secret key for API authentication.
        """
        if bot_token is None:
            raise ValueError("`bot_token` must be provided in constructor or in environment variable")
        super().__init__(bot_token)


    ###  Network fucntionality  ###


    async def get(
        self,
        endpoint: str="", *,
        url_params: dict[str, str]|None = None
    ):
        """
        Send GET request to the bot API.
        
        :param endpoint: url part after `api_url`
        :param url-params: ?xxx&yyy params of get-request (if needed)
        """
        url = f"{MAX_API_URL}/{endpoint}"
        headers = {
            "Authorization": self.bot_token
        }
        response: httpx.Response
        async with httpx.AsyncClient() as client:
            response = await client.get(
                url,
                headers=headers,
                params=url_params
            )
            response.raise_for_status()
        return response.json()



    async def patch(
        self,
        endpoint: str="", *,
        data: dict|None = None
    ):
        """
        Send PATCH request to the bot API.

        :param: endpoint: url part after `api_url`
        :param: data: request body in dict format
        """
        url = f"{MAX_API_URL}/{endpoint}"
        headers = {
            "Authorization": self.bot_token
        }
        response: httpx.Response
        async with httpx.AsyncClient() as client:
            response = await client.patch(
                url,
                headers=headers,
                json=data
            )
            response.raise_for_status()
        return response.json()



    async def post(
        self,
        endpoint: str="", *,
        data: dict|None = None,
        url_params: dict[str, str]|None = None
    ):
        """
        Send POST request to the bot API.

        :param: endpoint: url part after `api_url`
        :param: data: request body in dict format
        """
        url = f"{MAX_API_URL}/{endpoint}"
        headers = {
            "Authorization": self.bot_token
        }
        response: httpx.Response
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                headers=headers,
                params=url_params,
                json=data
            )
            response.raise_for_status()
        return response.json()
    

    async def delete(
        self,
        endpoint: str="", *,
        url_params: dict[str, str]|None = None
    ):
        """
        Send DELETE request to the bot API.

        :param: endpoint: url part after `api_url`
        """
        url = f"{MAX_API_URL}/{endpoint}"
        headers = {
            "Authorization": self.bot_token
        }
        response: httpx.Response
        async with httpx.AsyncClient() as client:
            response = await client.delete(
                url,
                headers=headers,
                params=url_params
            )
            response.raise_for_status()
        return response.json()
        


    ### Public Interfaces ###


    # Bot info & settings


    async def get_bot_info(self) -> dict:
        """
        Get info about the MAX Bot.
        """
        endpoint = "me"
        response = await self.get(endpoint)
        return response



    async def get_webhooks(self) -> dict:
        """
        Get webhooks for the MAX Bot.
        """
        endpoint = "subscriptions"
        response = await self.get(endpoint)
        return response



    async def start_webhooks(self, url: str) -> dict:
        """
        Start webhooks for the MAX Bot.

        :param url: address of the webhooks processing server    
        """
        endpoint = "subscriptions"
        body = { "url": url }
        response = await self.post(endpoint, data=body)
        return response



    async def remove_webhook(self, url: str) -> dict:
        """
        Remove existing webhook for the MAX Bot.
        """
        endpoint = "subscriptions"
        params = { "url": url }
        response = await self.delete(endpoint, url_params=params)
        return response



    async def get_bot_commands(self) -> list[dict]:
        """
        Get list of bot commands.
        """
        endpoint = "me"
        response = await self.get(endpoint)
        if "commands" in response:
            return response["commands"]
        return []
    


    async def register_command(self, *, name: str, description: str):
        """
        Register new command for the MAX Bot (/xxx).
        
        :param name: command name (without /)
        :param description: Command description
        """
        endpoint = "me"
        commands = await self.get_bot_commands()
        # Check if command already exists
        for command in commands:
            if command["name"] == name:
                raise ValueError(f"Command `{name}` already exists")
        # Register new command
        new_command = {
            "name": name,
            "description": description
        }
        commands.append(new_command)
        data = {
            "commands": commands
        }
        response = await self.patch(endpoint, data=data)
        return response



    async def remove_command(self, *, name: str):
        """
        Remove command from the MAX Bot.
        
        :param name: command name (without /)
        :raises ValueError: If command not found
        :raises httpx.NetworkError: If there's a network-related error during the request.
        """
        endpoint = "me"
        commands = await self.get_bot_commands()
        # Remake the commands list without element with key = <name> by list comprehension
        commands2 = [command for command in commands if command["name"] != name]
        # If nothing happened print "nothing happened"
        if commands == commands2:
            raise ValueError(f"Command `{name}` not found")
        data = {
            "commands": commands2
        }
        response = await self.patch(endpoint, data=data)
        return response


    # Messages


    async def send_text_message(self, text: str, target: str):
        """
        Send text message to the MAX user / chat via API.
        
        :param message: text message to send
        :param target: chat_id
        :raises httpx.NetworkError: If there is a network-related error during the request.
        """
        endpoint = "messages"
        data = {
            "text": text
        }
        response = await self.post(endpoint, data=data, url_params={"chat_id": target})
        return response



    async def send_keyboard_message(self, text: str, target: str, keyboard: MaxKeyboard):
        """
        Send message with inline keyboard to the MAX user / chat via API.
        
        :param message: text message to send
        :param target: chat_id
        :keyboard: 2d-array of buttons       
        """
        endpoint = "messages"
        data = {
            "text": text,
            "attachments": [
                {
                    "type": "inline_keyboard",
                    "payload": json.loads(keyboard.to_json())
                }
            ]
        }
        response = await self.post(endpoint, data=data, url_params={"chat_id": target})
        return response




###   End of class MaxSender   ###
