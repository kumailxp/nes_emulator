"""
This is the main file for the OLC6502 emulator.
"""
import enum
import numpy as np
from bus import Bus
from isa import LookupTable

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

RequiresExtraCycle = bool

class Olc6502:
    """
    Represents the 6502 processor in the NES emulator.

    The 6502 processor is responsible for executing instructions and managing the state of the NES.

    Attributes:
        a: Accumulator Register
        x: X Register
        y: Y Register
        stkp: Stack Pointer
        pc: Program Counter
        status: Status Register
        bus: Bus object for accessing memory
        memory: Memory array for storing data
    """

    def __init__(self, bus: Bus):
        """
        Initializes the olc6502 object.

        The olc6502 object represents the 6502 processor in the NES emulator. It contains registers,
        flags, and memory addresses for managing the state of the processor.

        Parameters:
            bus: The Bus object for accessing memory.

        Returns:
            None
        """
        self.a = 0
        self.x = 0
        self.y = 0
        self.stkp = 0
        self.pc = 0
        self.status = 0
        self.bus = bus

        # Memory
        self.memory = np.zeros(64 * 1024, dtype=int)

        # Absolute Address
        self.addr_abs: int = 0
        # Absolute Address
        self.addr_abs: int = 0

        # Relative Address
        self.addr_rel: int = 0

        # Current Opcode
        self.opcode: int = 0

        # Current Cycles
        self.cycles: int = 0
        # Relative Address
        self.addr_rel: int = 0

        # Current Opcode
        self.opcode: int = 0

        # Current Cycles
        self.cycles: int = 0

    def read(self, addr):
        """
        Read data from the specified address.

        Args:
            addr: The address to read from.

        Returns:
            The data read from the address.
        """
        return self.bus.read(addr)

    def write(self, addr, data):
        """
        Write data to the specified address.

        Args:
            addr: The address to write to.
            data: The data to write.
        """
        self.bus.write(addr, data)

    def get_flag(self, flag):
        """
        Get the value of the specified flag.

        Args:
            flag: The flag to get.

        Returns:
            The value of the flag.
        """
        return self.status & flag

    def set_flag(self, flag, value):
        """
        Set the value of the specified flag.

        Args:
            flag: The flag to set.
            value: The value to set the flag to.
        """
        if value:
            self.status |= flag
        else:
            self.status &= ~flag

    def clock(self):
        """
        Executes one clock cycle of the 6502 processor.

        This method is responsible for fetching the opcode, incrementing the program counter,
        and executing the instruction associated with the opcode.

        """
        if self.cycles == 0:
            self.opcode = self.read(self.pc)
            self.pc += 1
            self.cycles = LookupTable.lookup_table[self.opcode].cycles

    # Addressing Modes
    def imp(self) -> RequiresExtraCycle:
        """
        Implied addressing mode.

        This addressing mode does not require an address,
        as the instruction operates on the implied register.
        """
        return False

    def imm(self) -> RequiresExtraCycle:
        """
        Immediate addressing mode.

        This addressing mode uses the next byte as the address.
        """
        self.pc += 1
        self.addr_abs = self.pc
        return False

    def zp0(self) -> RequiresExtraCycle:
        """
        Zero Page addressing mode.

        This addressing mode uses the next byte as the address.
        """
        self.addr_abs = self.read(self.pc)
        self.pc += 1
        self.addr_abs &= 0x00FF
        return False

    def zpx(self) -> RequiresExtraCycle:
        """
        Zero Page X addressing mode.

        This addressing mode uses the next byte as the address, then adds the X register to it.
        """
        self.addr_abs = (self.read(self.pc) + self.x) & 0x00FF
        self.pc += 1
        return False

    def zpy(self) -> RequiresExtraCycle:
        """
        Zero Page Y addressing mode.

        This addressing mode uses the next byte as the address, then adds the Y register to it.
        """
        self.addr_abs = (self.read(self.pc) + self.y) & 0x00FF
        self.pc += 1
        return False

    def rel(self) -> RequiresExtraCycle:
        """
        Relative addressing mode.

        This addressing mode uses the next byte as the address, then adds it to the program counter.
        This address mode is exclusive to branch instructions. The address must reside within
        -128 to +127 of the branch instruction, i.e. you cant directly branch to any address in 
        the addressable range.
        """
        self.addr_rel = self.read(self.pc)
        self.pc += 1
        if self.addr_rel & 0x80:
            self.addr_rel |= 0xFF00
        return False

    def abs(self) -> RequiresExtraCycle:
        """
        Absolute addressing mode.

        This addressing mode uses the next two bytes as the address.
        """
        lo = self.read(self.pc)
        self.pc += 1
        hi = self.read(self.pc)
        self.pc += 1
        self.addr_abs = (hi << 8) | lo
        return False

    def abx(self) -> RequiresExtraCycle:
        """
        Absolute X addressing mode.

        This addressing mode uses the next two bytes as the address, then adds the X register to it.
        """
        lo = self.read(self.pc)
        self.pc += 1
        hi = self.read(self.pc)
        self.pc += 1
        self.addr_abs = (hi << 8) | lo
        self.addr_abs += self.x
        return True if (self.addr_abs & 0xFF00) != (hi << 8) else False

    def aby(self) -> RequiresExtraCycle:
        """
        Absolute Y addressing mode.

        This addressing mode uses the next two bytes as the address,
        then adds the Y register to it.
        """
        lo = self.read(self.pc)
        self.pc += 1
        hi = self.read(self.pc)
        self.pc += 1
        self.addr_abs = (hi << 8) | lo
        self.addr_abs += self.y
        return True if (self.addr_abs & 0xFF00) != (hi << 8) else False

    def ind(self) -> RequiresExtraCycle:
        """
        Indirect addressing mode.

        This addressing mode uses the next two bytes as the address,
        then reads the address from that location.
        """
        ptr_lo = self.read(self.pc)
        self.pc += 1
        ptr_hi = self.read(self.pc)
        self.pc += 1
        ptr = (ptr_hi << 8) | ptr_lo

        if ptr_lo == 0x00FF:
            self.addr_abs = (self.read(ptr & 0xFF00) << 8) | self.read(ptr)
        else:
            self.addr_abs = (self.read(ptr + 1) << 8) | self.read(ptr)
        return False

    def izx(self):
        """
        Indexed Indirect X addressing mode.

        This addressing mode uses the next byte as the address, then adds the X register to it.
        """
        t = self.read(self.pc)
        self.pc += 1
        lo = self.read((t + self.x) & 0x00FF)
        hi = self.read((t + self.x + 1) & 0x00FF)
        self.addr_abs = (hi << 8) | lo
        return False

    def izy(self):
        """
        Indirect Indexed Y addressing mode.

        This addressing mode uses the next byte as the address, then adds the Y register to it.
        """
        t = self.read(self.pc)
        self.pc += 1
        lo = self.read(t)
        hi = self.read((t + 1) & 0x00FF)
        self.addr_abs = (hi << 8) | lo
        self.addr_abs += self.y
        return True if (self.addr_abs & 0xFF00) != hi << 8 else False
