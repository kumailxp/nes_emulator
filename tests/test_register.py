""" 
Unit tests for the Register class.
"""

import pytest
from numpy import uint8, uint16
from nes.register import Register
from nes.flags import Flags

# pylint: disable=redefined-outer-name

@pytest.fixture
def register():
    """
    Pytest fixture to create an instance of the Register class.
    """
    return Register(a=uint8(0), x=uint8(0), y=uint8(0), stkp=uint8(0),
                    pc=uint16(0), status=uint8(0))

def test_get_flag(register):
    """
    Test the get_flag method of the Register class.
    """
    register.status = 0b10101010  # Set the status register to a specific value

    # Test individual flags
    assert register.get_flag(Flags.C) == 0
    assert register.get_flag(Flags.Z) == 1
    assert register.get_flag(Flags.I) == 0
    assert register.get_flag(Flags.D) == 1
    assert register.get_flag(Flags.B) == 0
    assert register.get_flag(Flags.U) == 1
    assert register.get_flag(Flags.V) == 0
    assert register.get_flag(Flags.N) == 1
