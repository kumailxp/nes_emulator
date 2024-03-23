""""
This module contains the Register class, which represents the CPU registers in an NES emulator.
"""
import dataclasses
from numpy import uint8, uint16

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
