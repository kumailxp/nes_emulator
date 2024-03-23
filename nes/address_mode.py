"""
Copy-Left 2024 NES Emulator Project
"""
import enum

class AddressingMode(enum.Enum):
    """
    Represents the addressing modes used in the 6502 processor.

    The addressing modes are used to determine how the processor accesses memory for instructions.

    Attributes:
        IMP: Implied
        IMM: Immediate
        ZP0: Zero Page
        ZPX: Zero Page X
        ZPY: Zero Page Y
        REL: Relative
        ABS: Absolute
        ABX: Absolute X
        ABY: Absolute Y
        IND: Indirect
        IZX: Indexed Indirect X
        IZY: Indirect Indexed Y
    """

    IMP = 0
    IMM = 1
    ZP0 = 2
    ZPX = 3
    ZPY = 4
    REL = 5
    ABS = 6
    ABX = 7
    ABY = 8
    IND = 9
    IZX = 10
    IZY = 11
