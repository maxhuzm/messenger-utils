"""
Tests for Sender and Derived Classes

Info: to run the tests you should have env vars available:
- `MESSENGER_UTILS_MAX_BOT_TOKEN`   # MAX API token to interact with bot
- `MESSENGER_UTILS_CHAT_ID`         # The chat for send messages to
- `RUN_IGNORED`                   # Temporary env var to prevent skipping the file

Test call usage:
```
>>> RUN_IGNORED=true pytest tests/test_sender.py
```
"""

import pytest
import asyncio
import os
from loguru import logger
from messenger_utils.max.max_sender import MaxSender
from messenger_utils.max.max_keyboard import *
from . import MAX_TOKEN, CHAT_ID

if CHAT_ID is None:
    raise ValueError("MESSENGER_UTILS_CHAT_ID environment variable not set.")


pytestmark = pytest.mark.skipif(
    os.getenv("RUN_IGNORED") != "true",
    reason="Ignore sender tests file by default"
)

def test_remove_webhook():
    """Test for removing non-existing bot's webhooks request to MAX API."""
    assert MAX_TOKEN is not None and CHAT_ID is not None, "MESSENGER_UTILS_MAX_BOT_TOKEN & CHAT_ID environment variable not set"
    sender = MaxSender(bot_token=MAX_TOKEN)
    response = asyncio.run(sender.remove_webhook(url="https://non-existing-url.com"))
    assert response.get("success") is False


@pytest.mark.skip(reason="Enable if want to test webhooks request")
def test_start_webhooks():
    """Test for starting bot's webhooks request to MAX API."""
    assert MAX_TOKEN is not None and CHAT_ID is not None, "MESSENGER_UTILS_MAX_BOT_TOKEN & CHAT_ID environment variable not set"
    sender = MaxSender(bot_token=MAX_TOKEN)
    response = asyncio.run(sender.start_webhooks(url="https://bot.gardenerio.ru/gardenbot"))
    assert response == {"success": True }


def test_send_message_with_attachments():
    """Test sending the message with inline buttons."""
    keyboard = MaxKeyboard()
    keyboard.add_row([
        CallbackButton(text="test1", payload="buttontoken"),
        LinkButton(text="test2", url="https://example.com")
    ])
    img_url = "https://bot.gardenerio.ru/energobot/images/energobot-title-image.png"
    assert MAX_TOKEN is not None and CHAT_ID is not None, "MESSENGER_UTILS_MAX_BOT_TOKEN & CHAT_ID environment variable not set"
    sender = MaxSender(bot_token=MAX_TOKEN)
    asyncio.run(sender.send_message(text="Test attachments", target=CHAT_ID, keyboard=keyboard, image_url=img_url))


def test_send_keyboard():
    """Test sending the message with inline button"""
    keyboard1 = MaxKeyboard(CallbackButton(text="test1", payload="buttontoken"))
    keyboard2 = MaxKeyboard([
        CallbackButton(text="test2", payload="buttontoken"),
        LinkButton(text="test3", url="https://example.com"),
        RequestContactButton(text="test4")
    ])
    keyboard3 = MaxKeyboard([
        [
            CallbackButton(text="test5", payload="buttontoken"),
            LinkButton(text="test6", url="https://example.com")
        ],
        [
            RequestContactButton(text="test7"),
            RequestGeoLocationButton(text="test8")
        ]
    ])
    assert MAX_TOKEN is not None and CHAT_ID is not None, "MESSENGER_UTILS_MAX_BOT_TOKEN environment variable not set"
    sender = MaxSender(bot_token=MAX_TOKEN)
    asyncio.run(sender.send_message(text="The keyboard1:", target=CHAT_ID, keyboard=keyboard1))
    asyncio.run(sender.send_message(text="The keyboard2:", target=CHAT_ID, keyboard=keyboard2))
    asyncio.run(sender.send_message(text="The keyboard3:", target=CHAT_ID, keyboard=keyboard3))
