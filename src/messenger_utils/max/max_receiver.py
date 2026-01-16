"""
Webhooks requests functionality for MAX API.
"""

from typing import Any, get_args
from messenger_utils.receiver import Receiver
from messenger_utils.models.max_webhook_event import EventTypes, MaxWebhookEventType, MaxWebhookEvent, MessageCreatedEvent, MessageCallbackEvent, Attachment
from . import logger



### Class MaxReceiver ###

class MaxReceiver(Receiver[MaxWebhookEventType]):
    """
    Webhooks requests processing for MAX API.
    """

    def __init__(self, webhook_data: dict[str, Any], bot_token: str|None = None):
        """
        Init MaxReceiver object.
        
        :param webhook_data: JSON-formatted message from messenger's webhook API
        :raises ValueError if the webhook body is not valid
        """
        super().__init__(webhook_data, bot_token)
        # Base check for MAX webhook body is valid
        if update_type := webhook_data.get("update_type") is None:
            raise ValueError("No `update_type` field in webhook body")
        valid_events = get_args(EventTypes)
        if update_type not in valid_events:
            raise ValueError("Unknown `update_type` value of webhook")
        self.webhook_event: MaxWebhookEventType | None  = None



    def parse_webhook(self) -> MaxWebhookEventType:
        """
        Parse webhook body stored in self.webhook_data.
        :return: Parsed webhook event object
        :raises ValueError if the webhook body is not valid
        """
        match self.webhook_data:
            # > Bot start or stop, dialog clear or remove
            case {
                "update_type": "bot_started" | "bot_stopped" | "dialog_cleared" | "dialog_removed",
                "timestamp": timestamp,
                "chat_id": chat_id,
                "user": user
            }:
                self.webhook_event = MaxWebhookEvent(
                    self.webhook_data["update_type"],
                    chat_id = chat_id,
                    user_id = user["user_id"],
                    user_name = user["name"],
                    user_is_bot = user["is_bot"],
                    timestamp = timestamp,
                    full_body = self.webhook_data
                )
            # > Message created
            case {
                "update_type": "message_created",
                "timestamp": timestamp,
                "message": {
                    "recipient": {
                        "chat_id": chat_id,
                        "user_id": bot_id
                    },
                    "sender": {
                        "user_id": user_id,
                        "name": user_name,
                        "is_bot": user_is_bot
                    },
                    "body": {
                        "text": text,
                        "attachments": attachments
                    }
                }
            }:
                self.webhook_event = MessageCreatedEvent(
                    "message_created",
                    chat_id = chat_id,
                    user_id = user_id,
                    user_name = user_name,
                    user_is_bot = user_is_bot,
                    recipient_id = bot_id,
                    text = text,
                    timestamp = timestamp,
                    full_body = self.webhook_data
                )
                # Chcek attachments
                if attachments:
                    for a in attachments:
                        self.webhook_event.attachments.append(
                            Attachment(
                                attachment_type = a["type"],
                                url = a["payload"]["url"],
                                token = a["payload"]["token"]
                            )
                        )
            # > Button callback
            case {
                "update_type": "message_callback",
                "timestamp": timestamp,
                "message": {
                    "recipient": {
                        "chat_id": chat_id
                    }
                },
                "callback": {
                    "payload": payload,
                    "callback_id": callback_id,
                    "user": {
                        "user_id": user_id,
                        "name": user_name,
                        "is_bot": user_is_bot
                    }
                }
            }:
                self.webhook_event = MessageCallbackEvent(
                    "message_callback",
                    timestamp = timestamp,
                    chat_id = chat_id,
                    user_id = user_id,
                    user_name = user_name,
                    user_is_bot = user_is_bot,
                    callback_id = callback_id,
                    payload = payload,
                    full_body = self.webhook_data
                )
            # > Unknown webhook
            case _:
                raise ValueError("Unknown webhook type")
        # Return parsed webhook as object
        return self.webhook_event



    async def parse_webhook2(self) -> dict:
        """
        Parse event from MAX webhook.
        
        :param event: JSON-formatted request body from MAX webhook API
        """
        body = self.webhook_data
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
            event = MaxWebhookEvent(
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
        #
        if body["update_type"] == "bot_stopped":
            # Bot stopped
            event = MaxWebhookEvent(
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
        #
        if body["update_type"] == "dialog_cleared":
            # Dialog cleared
            event = MaxWebhookEvent(
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
        #
        if body["update_type"] == "dialog_removed":
            # Dialog removed
            event = MaxWebhookEvent(
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
        #
        if body["update_type"] == "message_callback":
            # Message callback"
            event = MessageCallbackEvent(
                "message_callback",
                chat_id = body["message"]["recipient"]["chat_id"],
                user_id = body["callback"]["user"]["user_id"],
                user_name = body["callback"]["user"]["name"],
                user_is_bot = body["callback"]["user"]["is_bot"],
                callback_id = body["callback"]["callback_id"],
                payload = body["callback"]["payload"],
                timestamp = body["timestamp"],
                full_body=body
            )
            if event.payload not in self.callback_messages_table:
                logger.warning(f"Callback for button `{event.payload}` not found!")
                return {
                    "result": "error",
                    "type": "callback-not-found",
                    "description": f"Callback for button `{event.payload}` not found!",
                    **result
                }
            btn_result = await self.callback_messages_table[event.payload](event, self.bot_token)
            return {
                "result": "ok",
                "description": f"Callback for button `{event.payload}` executed",
                "button_result": btn_result,
                **result
            }
        #
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
            # Parse attachments
            if "attachments" in body["message"]["body"]:
                for attachment in body["message"]["body"]["attachments"]:
                    att = Attachment(
                        attachment_type = attachment["type"],
                        url = attachment["payload"]["url"],
                        token = attachment["payload"]["token"]
                    )
                    event.attachments.append(att)
            # Parse commands
            if event.text.startswith("/"):
                # The Message is a command
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
                # The Message is a text or img, or voice, etc...
                if self.create_message_func:
                    await self.create_message_func(event, self.bot_token)
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
