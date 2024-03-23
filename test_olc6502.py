"""
Test the Olc6502 class.
"""

import pytest
from olc6502 import Olc6502
from bus import Bus

@pytest.fixture
def cpu():
    """
    Pytest fixture to create an instance of the CPU class.
    """
    bus = Bus()  # Create an instance of the Bus class
    return Olc6502(bus)  # Pass the bus instance as an argument to the Olc6502 constructor

# pylint: disable=redefined-outer-name

def test_write(cpu):
    """
    Test the write method of the CPU class.
    """
    addr = 0x2000
    data = 0xFF

    cpu.write(addr, data)

    assert cpu.read(addr) == data

def test_write_with_different_data(cpu):
    """
    Test the write method of the CPU class with different data.
    """
    addr = 0x3000
    data = 0xAA

    cpu.write(addr, data)

    assert cpu.read(addr) == data

def test_read(cpu):
    """
    Test the read method of the CPU class.
    """
    addr = 0x4000
    data = 0x55

    cpu.write(addr, data)

    assert cpu.read(addr) == data
