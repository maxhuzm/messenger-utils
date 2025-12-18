"""
Parcing and processing messenger's responses and web-hooks
"""

from abc import ABC, abstractmethod
from collections.abc import Callable
from functools import wraps
from typing import ParamSpec, TypeVar
from . import logger

### CLASS `Receiver` ###

class Receiver(ABC):
    """
    Receiver abstract class - parcing and processing responses and web-hooks.
    Particular functionality is implemented in derived classes.
    """

    def __init__(self):
        """
        Init Receiver object.
        """
        self.commands_table: dict[str, Callable] = {}    # Command <=> Function link (set by decorator `Command``)


    #  DECORATORS

    def command(self, cmd_name: str) -> Callable:
        """
        Decorator factory for commands processing.
        
        :param name: command name (without /) to process
        :return: Decorator function
        """
        def decorator(func: Callable) -> Callable:
            """The decorator itself."""
            self.commands_table[cmd_name] = func
            @wraps(func)
            def wrapper(*args, **kwargs) -> Callable:
                """Wrapper function."""
                return func(*args, **kwargs)
            return wrapper
        return decorator
    


    #  PUBLIC METHODS

    @abstractmethod
    def parse_webhook(self, message: dict) -> dict:
        """
        Parse message in webhooks requests.
        
        :param message: JSON-formatted message from messenger's webhook API
        """
        pass

