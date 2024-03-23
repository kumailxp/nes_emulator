""""
This module contains the Flags enum, which represents the flags
used in the status register of the 6502 processor.
"""
import enum

class Flags(enum.Enum):
    """
    Represents the flags used in the status register of the 6502 processor.

    The flags are used to indicate various conditions and control the behavior of the processor.

    Attributes:
        C: Carry Bit
        Z: Zero
        I: Disable Interrupts
        D: Decimal Mode (unused in this implementation)
        B: Break
        U: Unused
        V: Overflow
        N: Negative
    """

    C = 1 << 0
    Z = 1 << 1
    I = 1 << 2
    D = 1 << 3
    B = 1 << 4
    U = 1 << 5
    V = 1 << 6
    N = 1 << 7
