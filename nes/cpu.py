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
        raise NotImplementedError("method must be implemented by the subclass.")

    def write(self, addr: uint16, data: uint8) -> None:
        raise NotImplementedError("method must be implemented by the subclass.")

    def set_flag(self, flag: Flags, value: bool) -> None:
        raise NotImplementedError("method must be implemented by the subclass.")

    def get_flag(self, flag: Flags) -> uint8:
        raise NotImplementedError("method must be implemented by the subclass.")

    def clock(self) -> None:
        raise NotImplementedError("method must be implemented by the subclass.")

    def fetch(self) -> uint8:
        raise NotImplementedError("method must be implemented by the subclass.")
