"""
Webhooks requests functionality for MAX API.
"""

from typing import Any, get_args
from messenger_utils.receiver import Receiver
from messenger_utils.models.max_webhook_event import *
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
        if (update_type := webhook_data.get("update_type")) is None:
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
                    "body": body
                }
            }:
                self.webhook_event = MessageCreatedEvent(
                    "message_created",
                    chat_id = chat_id,
                    user_id = user_id,
                    user_name = user_name,
                    user_is_bot = user_is_bot,
                    recipient_id = bot_id,
                    text = body["text"],
                    timestamp = timestamp,
                    full_body = self.webhook_data
                )
                # Chcek attachments
                if (attachments := body.get("attachments", None)) is not None:
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
                raise ValueError("Cannot parse webhook body")
        # Return parsed webhook as object
        return self.webhook_event



    async def process_webhook(self, **kwargs):
        """Bind handler functions to the event."""
        if self.webhook_event is None:
            self.parse_webhook()
        assert self.webhook_event is not None
        event: MaxWebhookEventType = self.webhook_event
        if event is None:
            return
        match event:
            # Bind start & stop
            case MaxWebhookEvent(event_type="bot_started"):
                logger.info("Event `bot_started` recognized")
                if MaxReceiver.bot_started_func is not None:
                    await MaxReceiver.bot_started_func(event, **kwargs)
            case MaxWebhookEvent(event_type="bot_stopped"):
                logger.info("Event `bot_stopped` recognized")
                if MaxReceiver.bot_stopped_func is not None:
                    await MaxReceiver.bot_stopped_func(event, **kwargs)
            # Bind dialog cleared & removed
            case MaxWebhookEvent(event_type="dialog_cleared"):
                logger.info("Event `dialog_cleared` recognized")
                if MaxReceiver.chat_cleared_func is not None:
                    await MaxReceiver.chat_cleared_func(event, **kwargs)
            case MaxWebhookEvent(event_type="dialog_removed"):
                logger.info("Event `dialog_removed` recognized")
                if MaxReceiver.chat_removed_func is not None:
                    await MaxReceiver.chat_removed_func(event, **kwargs)
            # Button callback
            case MessageCallbackEvent(event_type="message_callback"):
                logger.info("Event `message_callback` recognized")
                if event.payload not in MaxReceiver.callback_messages_table:
                    logger.warning(f"Callback for button `{event.payload}` not found!")
                    return
                await MaxReceiver.callback_messages_table[event.payload](event, **kwargs)
            # Message created
            case MessageCreatedEvent(event_type="message_created"):
                if event.text.startswith("/"):
                    # The Message is a command
                    logger.info("Event `command` recognized")
                    command = event.text[1:]
                    if command not in MaxReceiver.commands_table:
                        logger.warning(f"Command `{command}` not found!")
                        return
                    await MaxReceiver.commands_table[command](event, **kwargs)
                else:
                    # The Message is a text or img, or voice, etc...
                    logger.info("Event `create_message` recognized")
                    if MaxReceiver.create_message_func is not None:
                        await MaxReceiver.create_message_func(event, **kwargs)
        return

### End of class Receiver ###
