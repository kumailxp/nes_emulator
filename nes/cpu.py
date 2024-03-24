"""
Interface class for CPU
"""

from numpy import uint8, uint16
from nes.register import Register
from nes.flags import Flags


class Cpu:
    """
    Represents the CPU of the NES emulator.

    The Cpu class is responsible for executing instructions and managing the state of the CPU.
    """

    def __init__(self):
        self.register = Register(
            a=uint8(0),
            x=uint8(0),
            y=uint8(0),
            stkp=uint8(0),
            pc=uint16(0),
            status=uint8(0),
        )

        # Absolute Address
        self.addr_abs: uint16 = uint16(0)

        # Relative Address
        self.addr_rel: uint16 = uint16(0)

        # Current Opcode
        self.opcode: uint8 = uint8(0)

        # Current Cycles
        self.cycles: uint8 = uint8(0)

        # Fetched Data
        self.fetched: uint8 = uint8(0)

    # pylint: disable=unused-argument
    # pylint: disable=missing-function-docstring
    def read(self, addr: uint16) -> uint8:
        return uint8(0)

    def write(self, addr: uint16, data: uint8) -> None:
        pass

    def set_flag(self, flag: Flags, value: bool) -> None:
        pass

    def get_flag(self, flag: Flags) -> uint8:
        return uint8(0)

    def clock(self) -> None:
        pass

    def fetch(self) -> uint8:
        return uint8(0)
