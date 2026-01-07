"""
Tests for Sender and Derived Classes
"""

import pytest
from messenger_utils.sender import Sender
from messenger_utils.max.max_keyboard import *


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


def test_create_keyboard():
    """Test for creating keyboard."""
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
    assert keyboard1.to_json() == """{"buttons": [[{"type": "callback", "text": "test1", "payload": "buttontoken", "intent": "default"}]]}"""
    assert keyboard2.to_json() == """{"buttons": [[{"type": "callback", "text": "test2", "payload": "buttontoken", "intent": "default"}], [{"type": "link", "text": "test3", "url": "https://example.com"}], [{"type": "request_contact", "text": "test4"}]]}"""
    assert keyboard3.to_json() == """{"buttons": [[{"type": "callback", "text": "test5", "payload": "buttontoken", "intent": "default"}, {"type": "link", "text": "test6", "url": "https://example.com"}], [{"type": "request_contact", "text": "test7"}, {"type": "request_geo_location", "text": "test8", "quick": false}]]}"""
