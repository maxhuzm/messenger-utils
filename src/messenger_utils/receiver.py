"""
Parcing and processing messenger's responses and web-hooks
"""

from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar
from collections.abc import Callable
from functools import wraps

# Generic types: for MAX & Telegram specific objects
T_WHOOK = TypeVar("T_WHOOK")    # WebHook type

### CLASS `Receiver` ###

class Receiver(ABC, Generic[T_WHOOK]):
    """
    Receiver abstract class - parcing and processing responses and web-hooks.
    Particular functionality is implemented in derived classes.
    """
    
    # Class vars

    # Decorated function pointers for webhooks
    # Commands
    commands_table: dict[str, Callable] = {}               # Command <=> Function link (set by decorator `command``)
    # Messages
    create_message_func: Callable | None = None
    callback_messages_table: dict[str, Callable] = {}      # Button's token <=> Function link (set by decorator `callback`)
    # Functions processing bot state changes
    bot_started_func: Callable | None = None
    bot_stopped_func: Callable | None = None
    chat_cleared_func: Callable | None = None
    chat_removed_func: Callable | None = None



    def __init__(self, webhook_data: dict[str, Any], bot_token: str|None = None):
        """
        Init Receiver object.
        """
        self.webhook_data: dict[str, Any] = webhook_data
        self.bot_token: str|None = bot_token
        self.api_url: str = ""



    #
    # DECORATORS FACTORY
    #

    @classmethod
    def command(cls, cmd_name: str) -> Callable:
        """
        Decorator factory for commands processing.
        
        :param name: command name (without /) to process
        :return: Decorator function
        """
        def decorator(func: Callable) -> Callable:
            """The decorator itself."""
            cls.commands_table[cmd_name] = func
            @wraps(func)
            def wrapper(*args, **kwargs) -> Callable:
                """Wrapper function."""
                return func(*args, **kwargs)
            return wrapper
        return decorator


    @classmethod
    def callback(cls, btn_token: str) -> Callable:
        """
        Decorator for `callback_message` processing function.
        
        :return: Decorator function
        """
        def decorator(func: Callable) -> Callable:
            """The decorator itself."""
            cls.callback_messages_table[btn_token] = func
            @wraps(func)
            def wrapper(*args, **kwargs) -> Callable:
                """Wrapper function."""
                return func(*args, **kwargs)
            return wrapper
        return decorator



    #
    # SIMPLE DECORATORS
    #


    @classmethod
    def create_message(cls, func: Callable) -> Callable:
        """
        Decorator for `create_message` processing function.
        
        :return: Wrapped function
        """
        cls.create_message_func = func
        return func



    @classmethod
    def bot_started(cls, func: Callable) -> Callable:
        """
        Decorator for `bot_started` processing function.
        
        :return: Wrapped function
        """
        cls.bot_started_func = func
        return func



    @classmethod
    def bot_stopped(cls, func: Callable) -> Callable:
        """
        Decorator for `bot_stopped` processing function.
        
        :return: Wrapped function
        """
        cls.bot_stopped_func = func
        return func



    @classmethod
    def chat_cleared(cls, func: Callable) -> Callable:
        """
        Decorator for `chat_cleared` processing function.
        
        :return: Wrapped function
        """
        cls.chat_cleared_func = func
        return func



    @classmethod
    def chat_removed(cls, func: Callable) -> Callable:
        """
        Decorator for `chat_removed` processing function.
        
        :return: Wrapped function
        """
        cls.chat_removed_func = func
        return func



    #  PUBLIC METHODS


    @abstractmethod
    def parse_webhook(self) -> T_WHOOK:
        """
        Parse message provided in webhooks requests.
        
        :param body: JSON-formatted message from messenger's webhook API
        """
        pass


    @abstractmethod
    async def process_webhook(self, **kwargs):
        """Call bound functions according to event type."""
        pass
