"""
Tests for Sender and Derived Classes
"""

import pytest
from messenger_utils.sender import Sender


def test_absctact_sender():
    """
    Test for preventing declaration of abstract class object 
    """
    with pytest.raises(TypeError):
        Sender()

