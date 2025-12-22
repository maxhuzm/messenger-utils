"""
Webhooks requests functionality for MAX API.
"""

from messenger_utils.receiver import Receiver
from messenger_utils.models.webhook_event import WebhookEvent, MessageCreatedEvent, MessageCallbackEvent
from . import logger



### Class MaxReceiver ###

class MaxReceiver(Receiver):
    """
    Webhooks requests processing for MAX API.
    """

    def __init__(self):
        """
        Init MaxReceiver object.
        """
        super().__init__()



    async def parse_webhook(self, body: dict) -> dict:
        """
        Parse event from MAX webhook.
        
        :param event: JSON-formatted request body from MAX webhook API
        """
        result = {
            "full_content": body,
        }
        if "update_type" not in body:
            logger.warning("Message of unknown type received!")
            return {
                "result": "error",
                "description": "Webhook message of unknown type received!",
                **result
            }
        # Parse event types
        if body["update_type"] == "bot_started":
            # Bot started
            event = WebhookEvent(
                "bot_started", 
                chat_id = body["chat_id"],
                user_id = body["user"]["user_id"],
                user_name = body["user"]["name"],
                user_is_bot = body["user"]["is_bot"],
                timestamp = body["timestamp"],
                full_body = body
            )
            if self.bot_started_func:
                await self.bot_started_func(event, self.bot_token)
            return {
                "result": "ok",
                "description": "Bot started",
                **result
            }
        if body["update_type"] == "bot_stopped":
            # Bot stopped
            event = WebhookEvent(
                "bot_stopped", 
                chat_id = body["chat_id"],
                user_id = body["user"]["user_id"],
                user_name = body["user"]["name"],
                user_is_bot = body["user"]["is_bot"],
                timestamp = body["timestamp"],
                full_body = body
            )
            if self.bot_stopped_func:
                await self.bot_stopped_func(event, self.bot_token)
            return {
                "result": "ok",
                "description": "Bot stopped",
                **result
            }
        if body["update_type"] == "dialog_cleared":
            # Dialog cleared
            event = WebhookEvent(
                "dialog_cleared",
                chat_id = body["chat_id"],
                user_id = body["user"]["user_id"],
                user_name = body["user"]["name"],
                user_is_bot = body["user"]["is_bot"],
                timestamp = body["timestamp"],
                full_body = body
            )
            if self.chat_cleared_func:
                await self.chat_cleared_func(event, self.bot_token)
            return {
                "result": "ok",
                "description": "Dialog cleared",
                **result
            }
        if body["update_type"] == "dialog_removed":
            # Dialog removed
            event = WebhookEvent(
                "dialog_removed",
                chat_id = body["chat_id"],
                user_id = body["user"]["user_id"],
                user_name = body["user"]["name"],
                user_is_bot = body["user"]["is_bot"],
                timestamp = body["timestamp"],
                full_body = body
            )
            if self.chat_removed_func:
                await self.chat_removed_func(event, self.bot_token)
            return {
                "result": "ok",
                "description": "Dialog removed",
                **result
            }
        if body["update_type"] == "message_created":
            # Message created
            event = MessageCreatedEvent(
                "message_created",
                chat_id = body["message"]["recipient"]["chat_id"],
                user_id = body["message"]["sender"]["user_id"],
                user_name = body["message"]["sender"]["name"],
                user_is_bot = body["message"]["sender"]["is_bot"],
                recipient_id = body["message"]["recipient"]["user_id"],
                text = (body["message"]["body"]["text"]).strip(),
                timestamp=body["timestamp"],
                full_body=body
            )
            if event.text.startswith("/"):
                # Message is a command
                command = event.text[1:]
                if command not in self.commands_table:
                    logger.warning(f"Command `{command}` not found!")
                    return {
                        "result": "error",
                        "type": "command-not-found",
                        "description": f"Command `{command}` not found!",
                        **result
                    }
                cmd_result = await self.commands_table[command](event, self.bot_token)
                return {
                    "result": "ok",
                    "description": f"Command `{command}` executed",
                    "command_result": cmd_result,
                    **result
                }
            else:
                # Message is a text or img, or voice, etc...
                return {
                    "result": "ok",
                    "description": "Message received",
                    "text": event.text,
                    **result
                }
        else:
            # Other message types
            return {
                "result": "ok",
                "description": "Event received",
                **result
            }


### End of class Receiver ###
