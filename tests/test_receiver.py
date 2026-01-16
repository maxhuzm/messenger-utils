"""
Tests for Receiver and Derived Classes

Info: to run the tests you should have env vars available:
- `MESSENGER_UTILS_MAX_BOT_TOKEN`   # MAX API token to interact with bot
"""

import pytest
from messenger_utils.max import MaxReceiver
from messenger_utils.models.max_webhook_event import MaxWebhookEvent, MessageCreatedEvent


def test_unknown_event():
    """Test for unknown event type."""
    body = {
        "update_type": "unknown"
    }
    with pytest.raises(ValueError):
        _ = MaxReceiver(webhook_data=body)


def test_cannot_parse_body():
    """Test for wrong webhook body."""
    body = {
        "update_type": "bot_started",
        "timestamp": 1767730065426,
        # no rest params
    }
    receiver = MaxReceiver(webhook_data=body)
    with pytest.raises(ValueError):
        receiver.parse_webhook()


def test_bot_started():
    """Test for bot_starded event."""
    body = {
        "timestamp": 1767730065426,
        "chat_id": 94154102,
        "user": {
            "user_id": 59483360,
            "first_name": "Maxim",
            "last_name": "",
            "is_bot": False,
            "last_activity_time": 1767730058000,
            "avatar_url": "https://i.oneme.ru/i?r=BUFglOvkF6bn--g5U-BFgIkJBWtfbbZGTyD8N6aOjR3s2_bNqhlH9vK-tLWrDL6kek3GFH9N3ZZiJT4VUTauAyqj",
            "full_avatar_url": "https://i.oneme.ru/i?r=BTFjO43w8Yr1OSJ4tcurq5HipGcKd8uUvjOWb39WvY8JpOcc-8lS4YvZ24Vub5ymKiQ",
            "name": "Maxim"
        },
        "user_locale": "ru",
        "user_id": 59483360,
        "update_type": "bot_started"
    }
    receiver = MaxReceiver(webhook_data=body)
    event = receiver.parse_webhook()
    assert isinstance(event, MaxWebhookEvent)
    assert event.event_type == "bot_started"
    assert event.chat_id == 94154102
    assert event.user_id == 59483360
    assert event.user_name == "Maxim"
    assert event.user_is_bot is False
    assert event.timestamp == 1767730065426


def test_bot_stopped():
    """Test for bot_stopped event."""
    body = {
        "chat_id": 100052860,
        "user": {
            "user_id": 59483360,
            "first_name": "Maxim",
            "last_name": "",
            "is_bot": False,
            "last_activity_time": 1764673805000,
            "name": "Maxim"
        },
        "timestamp": 1764673811705,
        "user_locale": "ru",
        "update_type": "bot_stopped"
    }
    receiver = MaxReceiver(webhook_data=body)
    event = receiver.parse_webhook()
    assert isinstance(event, MaxWebhookEvent)
    assert event.event_type == "bot_stopped"
    assert event.chat_id == 100052860
    assert event.user_id == 59483360
    assert event.user_name == "Maxim"
    assert event.user_is_bot is False
    assert event.timestamp == 1764673811705


def test_message_created():
    """Test for message_created event."""
    body = {
        "timestamp": 1764671262844,
        "message": {
            "recipient": {
                "chat_id": 100052860,
                "chat_type": "dialog",
                "user_id": 108858268
            },
            "timestamp": 1764671262844,
            "body": {
                "mid": "mid.0000000005f6af7c019ade9a907c08ef",
                "seq": 115649495881746671,
                "text": "Hello"
            },
            "sender": {
                "user_id": 59483360,
                "first_name": "Maxim",
                "last_name": "",
                "is_bot": False,
                "last_activity_time": 1764670619000,
                "name": "Maxim"
            }
        },
        "user_locale": "ru",
        "update_type": "message_created"
    }
    receiver = MaxReceiver(webhook_data=body)
    event = receiver.parse_webhook()
    assert isinstance(event, MessageCreatedEvent)
    assert event.event_type == "message_created"
    assert event.chat_id == 100052860
    assert event.user_id == 59483360
    assert event.text == "Hello"


def test_message_attachments():
    """Test for message_created event."""
    body = {
        "timestamp": 1764671262844,
        "message": {
            "recipient": {
                "chat_id": 100052860,
                "chat_type": "dialog",
                "user_id": 108858268
            },
            "timestamp": 1764671262844,
            "body": {
                "mid": "mid.0000000005f6af7c019ade9a907c08ef",
                "seq": 115649495881746671,
                "text": "Hello",
                "attachments": [
                {
                    "payload": {
                        "photo_id": 872509408,
                        "token": "t3c925YlGVyqXqa2NOpP39V+Fl14BbVLyd0/JEhhGA9UYI1EmHNSHZqJM1vhFaCyUIU69jc/Beg+jzXQeS+8R99gWJxrJw0l",
                        "url": "https://i.oneme.ru/i?r=BTGBPUwtwgYUeoFhO7rESmr8hY9gd4KKV5mzHmI277kTyNMW-5WsPYR_ZaEeuveXSk0"
                    },
                    "type": "image"
                },
                {
                    "payload": {
                        "url": "http://vd375.okcdn.ru/?expires=1766397298872&pr=96&srcAg=UNKNOWN&ms=45.136.22.80&type=2&sig=0bGw58LTgpU&ct=2&urls=45.136.21.7&clientType=11&appId=1248243456&id=9652826213118",
                        "token": "f9LHodD0cOJ03QqaX5M3H7BKLCQ9X_KptTbylZZi3NegengGTDOw6WF8IneV-5iQ68FuQsIulMbjTu2mo4tj",
                        "id": 10254804476158
                    },
                    "type": "audio"
                }
            ]
            },
            "sender": {
                "user_id": 59483360,
                "first_name": "Maxim",
                "last_name": "",
                "is_bot": False,
                "last_activity_time": 1764670619000,
                "name": "Maxim"
            }
        },
        "user_locale": "ru",
        "update_type": "message_created"
    }
    receiver = MaxReceiver(webhook_data=body)
    event = receiver.parse_webhook()
    assert isinstance(event, MessageCreatedEvent)
    assert event.event_type == "message_created"
    assert event.attachments[0].attachment_type == "image"
    assert event.attachments[1].attachment_type == "audio"
