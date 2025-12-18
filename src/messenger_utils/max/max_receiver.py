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



    def parse_webhook(self, message: dict) -> dict:
        """
        Parse message from MAX webhook.
        
        :param message: JSON-formatted message from MAX webhook API
        """
        result = {
            "full_content": message,
        }
        if "update_type" not in message:
            logger.warning("Message of unknown type received!")
            return {
                "result": "error",
                "description": "Webhook message of unknown type received!",
                **result
            }
        # Parse message types
        if message["update_type"] == "message_created":
            # Message created
            content: str = message["message"]["body"]["text"]
            if content.startswith("/"):
                # Message is a command
                command = content[1:]
                if command not in self.commands_table:
                    logger.warning(f"Command `{command}` not found!")
                    return {
                        "result": "error",
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
