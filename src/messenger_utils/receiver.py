"""
Parcing and processing messenger's responses and web-hooks
"""

from abc import ABC, abstractmethod


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
        pass