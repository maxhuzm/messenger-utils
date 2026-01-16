"""
MAX messenger inits.
"""
MAX_API_URL = "https://platform-api.max.ru"

from .. import logger
from .max_sender import MaxSender
from .max_receiver import MaxReceiver
from .max_keyboard import MaxKeyboard, CallbackButton
from ..models.max_webhook_event import MaxWebhookEventType, MaxWebhookEvent, MessageCreatedEvent, MessageCallbackEvent, EventTypes


__all__ = [
    "logger",
    "MAX_API_URL",
    "MaxSender",
    "MaxReceiver",
    "MaxKeyboard",
    "CallbackButton",
    "MaxWebhookEvent",
    "MaxWebhookEventType",
    "MessageCreatedEvent",
    "MessageCallbackEvent",
    "EventTypes"
]
