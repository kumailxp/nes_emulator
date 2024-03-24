import pytest
from nes.instruction_selector import InstructionSelector
from nes.bus import Bus
from nes.olc6502 import Olc6502
from nes.flags import Flags


@pytest.fixture
def cpu():
    """
    Pytest fixture to create an instance of the CPU class.
    """
    bus = Bus()  # Create an instance of the Bus class
    return Olc6502(bus)  # Pass the bus instance as an argument to the Olc6502 constructor

# pylint: disable=redefined-outer-name
# pylint: disable=invalid-name
def test_CLC(cpu: Olc6502):
    """
    Test the CLC instruction.
    """
    selector = InstructionSelector(cpu)
    test_cpu = selector.cpu

    # Set the carry flag to True
    test_cpu.set_flag(Flags.C, True)

    # Execute the CLC instruction
    selector.CLC()

    # Check if the carry flag is cleared
    assert test_cpu.get_flag(Flags.C) == 0