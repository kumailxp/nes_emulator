""""
This module contains the Register class, which represents the CPU registers in an NES emulator.
"""
import dataclasses
from numpy import uint8, uint16
from nes.flags import Flags

@dataclasses.dataclass
class Register:
    """
    Represents the CPU registers in an NES emulator.

    Attributes:
        a (int): The accumulator register.
        x (int): The X register.
        y (int): The Y register.
        stkp (int): The stack pointer register.
        pc (int): The program counter register.
        status (int): The status register.
    """
    a: uint8
    x: uint8
    y: uint8
    stkp: uint8
    pc: uint16
    status: uint8

    def __str__(self) -> str:
        return f"Register(a={self.a}, x={self.x}, y={self.y}, \
                stkp={self.stkp}, pc={self.pc}, status={self.status})"

    def __repr__(self) -> str:
        return str(self)

    def get_flag(self, flag: Flags) -> uint8:
        """
        Retrieves the value of the specified flag from the status register.

        Args:
            flag (Flags): The flag to retrieve the value of.

        Returns:
            uint8: The value of the specified flag (1 if set, 0 if not set).
        """
        return uint8(1) if self.status & uint8(flag.value) > 0 else uint8(0)

    def set_flag(self, flag: Flags, value: bool) -> None:
        """
        Sets the specified flag in the status register to the given value.

        Args:
            flag (Flags): The flag to be set.
            value (bool): The value to set the flag to.
        """
        if value:
            self.status |= uint8(flag.value)
        else:
            self.status &= ~flag.value # pylint: disable=*
