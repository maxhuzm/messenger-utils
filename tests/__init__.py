"""
Tests init.
"""

import os

MAX_TOKEN = os.getenv("MESSENGER_UTILS_MAX_BOT_TOKEN")
if MAX_TOKEN is None:
    raise ValueError("MESSENGER_UTILS_MAX_BOT_TOKEN environment variable not set.")

CHAT_ID = 94154102
