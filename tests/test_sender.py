"""
Tests for Sender and Derived Classes
"""

import asyncio
import pytest
from messenger_utils.sender import Sender
from messenger_utils.max.max_sender import MaxSender
from messenger_utils.max.max_keyboard import *
from . import MAX_TOKEN, CHAT_ID


def test_absctact_sender():
    """Test for preventing declaration of abstract class object."""
    with pytest.raises(TypeError):
        Sender()


def test_button_types():
    """Test for the button of diff types get btn_type correctly."""
    callback_btn = CallbackButton(text="test", payload="buttontoken")
    assert callback_btn.btn_type == BtnTypes.CALLBACK
    link_btn = LinkButton(text="test", url="https://example.com")
    assert link_btn.btn_type == BtnTypes.LINK
    request_contact_btn = RequestContactButton(text="test")
    assert request_contact_btn.btn_type == BtnTypes.REQUEST_CONTACT
    request_geo_location_btn = RequestGeoLocationButton(text="test")
    assert request_geo_location_btn.btn_type == BtnTypes.REQUEST_GEO_LOCATION
    open_app_btn = OpenAppButton(text="test")
    assert open_app_btn.btn_type == BtnTypes.OPEN_APP
    message_btn = MessageButton("test")
    assert message_btn.btn_type == BtnTypes.MESSAGE


def test_button_serialize():
    """Test the output dictionary when buttons serialized."""
    callback_btn = CallbackButton(text="test", payload="buttontoken")
    callback_btn_dict = callback_btn.to_json()
    assert callback_btn_dict == '{"type": "callback", "text": "test", "payload": "buttontoken", "intent": "default"}'
    request_geo_location_btn = RequestGeoLocationButton(text="test", quick=True)
    request_geo_location_btn_dict = request_geo_location_btn.to_json()
    assert request_geo_location_btn_dict == '{"type": "request_geo_location", "text": "test", "quick": true}'
    open_app_btn = OpenAppButton(text="test", web_app="web_app", payload="payload", contact_id=123)
    open_app_btn_dict = open_app_btn.to_json()
    assert open_app_btn_dict == '{"type": "open_app", "text": "test", "web_app": "web_app", "contact_id": 123, "payload": "payload"}'


def test_remove_webhook():
    """Test for removing non-existing bot's webhooks request to MAX API."""
    assert MAX_TOKEN is not None, "MESSENGER_UTILS_MAX_BOT_TOKEN environment variable not set"
    sender = MaxSender(bot_token=MAX_TOKEN)
    response = asyncio.run(sender.remove_webhook(url="https://non-existing-url.com"))
    assert response.get("success") is False


@pytest.mark.skip(reason="Enable if want to test webhooks request")
def test_start_webhooks():
    """Test for starting bot's webhooks request to MAX API."""
    assert MAX_TOKEN is not None, "MESSENGER_UTILS_MAX_BOT_TOKEN environment variable not set"
    sender = MaxSender(bot_token=MAX_TOKEN)
    response = asyncio.run(sender.start_webhooks(url="https://bot.gardenerio.ru/gardenbot"))
    assert response == {"success": True }


@pytest.mark.skip(reason="Enable if want to send message")
def test_send_message_with_attachments():
    """Test sending the message with inline buttons."""
    keyboard = MaxKeyboard()
    keyboard.add_row([
        CallbackButton(text="test1", payload="buttontoken"),
        LinkButton(text="test2", url="https://example.com")
    ])
    img_url = "https://bot.gardenerio.ru/gardenbot-title-image.png"
    assert MAX_TOKEN is not None, "MESSENGER_UTILS_MAX_BOT_TOKEN environment variable not set"
    sender = MaxSender(bot_token=MAX_TOKEN)
    asyncio.run(sender.send_message(text="Test attachments", target=CHAT_ID, keyboard=keyboard, image_url=img_url))



@pytest.mark.skip(reason="Enable if want to send message with keyboard")
def test_send_keyboard():
    """Test sending the message with inline button"""
    keyboard = MaxKeyboard()
    keyboard.add_row([
        CallbackButton(text="test1", payload="buttontoken"),
        LinkButton(text="test2", url="https://example.com")
    ])
    keyboard.add_row([
        RequestContactButton(text="test3"),
        RequestGeoLocationButton(text="test4")
    ])
    keyboard.add_row([
        MessageButton(text="test6")
    ])
    assert MAX_TOKEN is not None, "MESSENGER_UTILS_MAX_BOT_TOKEN environment variable not set"
    sender = MaxSender(bot_token=MAX_TOKEN)
    asyncio.run(sender.send_keyboard_message(text="test", target=CHAT_ID, keyboard=keyboard))
