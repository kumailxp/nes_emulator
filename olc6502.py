"""
This is the main file for the OLC6502 emulator.
"""
from numpy import uint8, uint16
from bus import Bus
from isa import LookupTable
from address_mode import AddressingMode
from register import Register

RequiresExtraCycle = bool


class Olc6502:
    """
    Represents the 6502 processor in the NES emulator.

    The 6502 processor is responsible for executing instructions and managing the state of the NES.

    Attributes:
        bus: Bus object for accessing memory
        memory: Memory array for storing data
    """

    mode_lookup = {
        AddressingMode.IMP: lambda self: self.imp(),
        AddressingMode.IMM: lambda self: self.imm(),
        AddressingMode.ZP0: lambda self: self.zp0(),
        AddressingMode.ZPX: lambda self: self.zpx(),
        AddressingMode.ZPY: lambda self: self.zpy(),
        AddressingMode.REL: lambda self: self.rel(),
        AddressingMode.ABS: lambda self: self.abs(),
        AddressingMode.ABX: lambda self: self.abx(),
        AddressingMode.ABY: lambda self: self.aby(),
        AddressingMode.IND: lambda self: self.ind(),
        AddressingMode.IZX: lambda self: self.izx(),
        AddressingMode.IZY: lambda self: self.izy(),
    }

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
        self.register = Register(
            a=uint8(0),
            x=uint8(0),
            y=uint8(0),
            stkp=uint8(0),
            pc=uint16(0),
            status=uint8(0),
        )

        self.bus = bus

        # Memory
        # self.memory = np.zeros(64 * 1024, dtype=uint8)

        # Absolute Address
        self.addr_abs: uint16 = uint16(0)

        # Relative Address
        self.addr_rel: uint16 = uint16(0)

        # Current Opcode
        self.opcode: uint8 = uint8(0)

        # Current Cycles
        self.cycles: uint8 = uint8(0)

    def get_register(self):
        """
        Get the register object.

        Returns:
            The register object.
        """
        return self.register

    def read(self, addr : uint16) -> uint8:
        """
        Read data from the specified address.

        Args:
            addr: The address to read from.

        Returns:
            The data read from the address.
        """
        return self.bus.read(addr)

    def write(self, addr: uint16, data: uint8) -> None:
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
        return self.get_register().status & flag

    def set_flag(self, flag, value):
        """
        Set the value of the specified flag.

        Args:
            flag: The flag to set.
            value: The value to set the flag to.
        """
        if value:
            self.get_register().status |= flag
        else:
            self.get_register().status &= ~flag

    def clock(self):
        """
        Executes one clock cycle of the 6502 processor.

        This method is responsible for fetching the opcode, incrementing the program counter,
        and executing the instruction associated with the opcode.

        """
        if self.cycles == 0:
            self.opcode = self.read(self.get_register().pc)
            self.get_register().pc += 1
            instruction = LookupTable.lookup_table[self.opcode]
            self.cycles = instruction.cycles

            # require_extra_cycle_from_mode = Olc6502.mode_lookup[instruction.addr_mode](self)
            # require_extra_cycle_from_instruction = instruction.execute()

    def execute(self):
        """
        Executes the instruction associated with the current opcode.

        This method is responsible for executing the instruction associated with the current opcode.
        """
        instruction = LookupTable.lookup_table[self.opcode]

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
        self.get_register().pc += 1
        self.addr_abs = self.get_register().pc
        return False

    def zp0(self) -> RequiresExtraCycle:
        """
        Zero Page addressing mode.

        This addressing mode uses the next byte as the address.
        """
        self.addr_abs =  uint16(self.read(self.get_register().pc))
        self.get_register().pc += 1
        self.addr_abs &= uint16(0x00FF)
        return False

    def zpx(self) -> RequiresExtraCycle:
        """
        Zero Page X addressing mode.

        This addressing mode uses the next byte as the address, then adds the X register to it.
        """
        self.addr_abs = uint16(self.read(self.get_register().pc) +
                                    self.get_register().x) & uint16(0x00FF)
        self.get_register().pc += 1
        return False

    def zpy(self) -> RequiresExtraCycle:
        """
        Zero Page Y addressing mode.

        This addressing mode uses the next byte as the address, then adds the Y register to it.
        """
        self.addr_abs = uint16(
            self.read(self.get_register().pc) + self.get_register().y
        ) & uint16(0x00FF)
        self.get_register().pc += 1
        return False

    def rel(self) -> RequiresExtraCycle:
        """
        Relative addressing mode.

        This addressing mode uses the next byte as the address, then adds it to the program counter.
        This address mode is exclusive to branch instructions. The address must reside within
        -128 to +127 of the branch instruction, i.e. you cant directly branch to any address in
        the addressable range.
        """
        self.addr_rel = uint16(self.read(self.get_register().pc))
        self.get_register().pc += 1
        if self.addr_rel & 0x80:
            self.addr_rel |= uint16(0xFF00)
        return False

    def abs(self) -> RequiresExtraCycle:
        """
        Absolute addressing mode.

        This addressing mode uses the next two bytes as the address.
        """
        lo = self.read(self.get_register().pc)
        self.get_register().pc += 1
        hi = self.read(self.get_register().pc)
        self.get_register().pc += 1
        self.addr_abs = uint16((hi << 8) | lo)
        return False

    def abx(self) -> RequiresExtraCycle:
        """
        Absolute X addressing mode.

        This addressing mode uses the next two bytes as the address, then adds the X register to it.
        """
        lo = self.read(self.get_register().pc)
        self.get_register().pc += 1
        hi = self.read(self.get_register().pc)
        self.get_register().pc += 1
        self.addr_abs = uint16((hi << 8) | lo)
        self.addr_abs += self.get_register().x
        return True if (self.addr_abs & 0xFF00) != (hi << 8) else False

    def aby(self) -> RequiresExtraCycle:
        """
        Absolute Y addressing mode.

        This addressing mode uses the next two bytes as the address,
        then adds the Y register to it.
        """
        lo = self.read(self.get_register().pc)
        self.get_register().pc += 1
        hi = self.read(self.get_register().pc)
        self.get_register().pc += 1
        self.addr_abs = uint16((hi << 8) | lo)
        self.addr_abs += self.get_register().y
        return True if (self.addr_abs & 0xFF00) != (hi << 8) else False

    def ind(self) -> RequiresExtraCycle:
        """
        Indirect addressing mode.

        This addressing mode uses the next two bytes as the address,
        then reads the address from that location.
        """
        ptr_lo = self.read(self.get_register().pc)
        self.get_register().pc += 1
        ptr_hi = self.read(self.get_register().pc)
        self.get_register().pc += 1
        ptr = uint16((ptr_hi << 8) | ptr_lo)

        if ptr_lo == 0x00FF:
            self.addr_abs = uint16(self.read(ptr & uint16(0xFF00)) << 8) | uint16(self.read(ptr))
        else:
            self.addr_abs = uint16(self.read(uint16(ptr + 1)) << 8) | uint16(self.read(ptr))
        return False

    def izx(self):
        """
        Indexed Indirect X addressing mode.

        This addressing mode uses the next byte as the address, then adds the X register to it.
        """
        t = self.read(self.get_register().pc)
        self.get_register().pc += 1
        lo = self.read((t + self.get_register().x) & uint16(0x00FF))
        hi = self.read((t + self.get_register().x + 1) & uint16(0x00FF))
        self.addr_abs = uint16((hi << 8) | lo)
        return False

    def izy(self):
        """
        Indirect Indexed Y addressing mode.

        This addressing mode uses the next byte as the address, then adds the Y register to it.
        """
        t = self.read(self.get_register().pc)
        self.get_register().pc += 1
        lo = self.read(uint16(t))
        hi = self.read((t + 1) & 0x00FF)
        self.addr_abs = uint16((hi << 8) | lo)
        self.addr_abs += self.get_register().y
        return True if (self.addr_abs & 0xFF00) != hi << 8 else False
