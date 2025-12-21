"""
Webhooks requests functionality for MAX API.
"""

from messenger_utils.receiver import Receiver
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



    def parse_webhook(self, event: dict) -> dict:
        """
        Parse event from MAX webhook.
        
        :param event: JSON-formatted request body from MAX webhook API
        """
        result = {
            "full_content": event,
        }
        if "update_type" not in event:
            logger.warning("Message of unknown type received!")
            return {
                "result": "error",
                "description": "Webhook message of unknown type received!",
                **result
            }
        # Parse event types
        if event["update_type"] == "bot_started":
            # Bot started
            if self.bot_started_func:
                self.bot_started_func()
            return {
                "result": "ok",
                "description": "Bot started",
                **result
            }
        if event["update_type"] == "bot_stopped":
            # Bot stopped
            if self.bot_stopped_func:
                self.bot_stopped_func()
            return {
                "result": "ok",
                "description": "Bot stopped",
                **result
            }
        if event["update_type"] == "dialog_cleared":
            # Dialog cleared
            if self.chat_cleared_func:
                self.chat_cleared_func()
            return {
                "result": "ok",
                "description": "Dialog cleared",
                **result
            }
        if event["update_type"] == "dialog_removed":
            # Dialog removed
            if self.chat_removed_func:
                self.chat_removed_func()
            return {
                "result": "ok",
                "description": "Dialog removed",
                **result
            }
        if event["update_type"] == "message_created":
            # Message created
            content: str = event["message"]["body"]["text"]
            if content.startswith("/"):
                # Message is a command
                command = content[1:]
                if command not in self.commands_table:
                    logger.warning(f"Command `{command}` not found!")
                    return {
                        "result": "error",
                        "type": "command-not-found",
                        "description": f"Command `{command}` not found!",
                        **result
                    }
                cmd_result = self.commands_table[command]()
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
                    "content": content,
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
