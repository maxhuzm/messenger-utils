"""
Tests init.
"""

import os

MAX_TOKEN = os.getenv("MESSENGER_UTILS_MAX_BOT_TOKEN")
if MAX_TOKEN is None:
    raise ValueError("MESSENGER_UTILS_MAX_BOT_TOKEN environment variable not set.")

CHAT_ID = os.getenv("MESSENGER_UTILS_CHAT_ID")
if CHAT_ID is None:
    raise ValueError("MESSENGER_UTILS_CHAT_ID environment variable not set.")
CHAT_ID = int(CHAT_ID)
