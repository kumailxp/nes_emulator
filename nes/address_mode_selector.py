"""
Addressing Mode Selector
"""

from numpy import uint16
from nes.cpu import Cpu
from nes.address_mode import AddressingMode

RequiresExtraCycle = bool
# pylint: disable=invalid-name
class AddressModeSelector:
    """
    The AddressModeSelector class is responsible for selecting the appropriate addressing mode
    for the instructions in the NES emulator.

    It provides methods for each addressing mode, such as implied, immediate, zero page, etc.,
    which return a boolean value indicating whether an extra cycle is required for the instruction.
    """

    def __init__(self, cpu: Cpu) -> None:
        self.cpu = cpu

    def select(self, mode: AddressingMode) -> RequiresExtraCycle:
        """
        Selects the appropriate addressing mode based on the given mode parameter.

        Args:
            mode (AddressingMode): The addressing mode to be selected.

        Returns:
            RequiresExtraCycle: The result of the selected addressing mode.
        """
        if mode not in AddressingMode:
            raise ValueError(f"Invalid addressing mode: {mode}")
        return getattr(self, AddressingMode(mode).name)()

    def IMP(self) -> RequiresExtraCycle:
        """
        Implied addressing mode.

        This addressing mode does not require an address,
        as the instruction operates on the implied register.
        """
        return False

    def IMM(self) -> RequiresExtraCycle:
        """
        Immediate addressing mode.

        This addressing mode uses the next byte as the address.
        """
        self.cpu.register.pc += 1
        self.cpu.addr_abs = self.cpu.register.pc
        return False

    def ZP0(self) -> RequiresExtraCycle:
        """
        Zero Page addressing mode.

        This addressing mode uses the next byte as the address.
        """
        self.cpu.addr_abs = uint16(self.cpu.read(self.cpu.register.pc))
        self.cpu.register.pc += 1
        self.cpu.addr_abs &= uint16(0x00FF)
        return False

    def ZPX(self) -> RequiresExtraCycle:
        """
        Zero Page X addressing mode.

        This addressing mode uses the next byte as the address, then adds the X register to it.
        """
        self.cpu.addr_abs = uint16(
            self.cpu.read(self.cpu.register.pc) + self.cpu.register.x
        ) & uint16(0x00FF)
        self.cpu.register.pc += 1
        return False

    def ZPY(self) -> RequiresExtraCycle:
        """
        Zero Page Y addressing mode.

        This addressing mode uses the next byte as the address, then adds the Y register to it.
        """
        self.cpu.addr_abs = uint16(
            self.cpu.read(self.cpu.register.pc) + self.cpu.register.y
        ) & uint16(0x00FF)
        self.cpu.register.pc += 1
        return False

    def REL(self) -> RequiresExtraCycle:
        """
        Relative addressing mode.

        This addressing mode uses the next byte as the address, then adds it to the program counter.
        This address mode is exclusive to branch instructions. The address must reside within
        -128 to +127 of the branch instruction, i.e. you cant directly branch to any address in
        the addressable range.
        """
        self.cpu.addr_rel = uint16(self.cpu.read(self.cpu.register.pc))
        self.cpu.register.pc += 1
        if self.cpu.addr_rel & 0x80:
            self.cpu.addr_rel |= uint16(0xFF00)
        return False

    def ABS(self) -> RequiresExtraCycle:
        """
        Absolute addressing mode.

        This addressing mode uses the next two bytes as the address.
        """
        lo = self.cpu.read(self.cpu.register.pc)
        self.cpu.register.pc += 1
        hi = self.cpu.read(self.cpu.register.pc)
        self.cpu.register.pc += 1
        self.cpu.addr_abs = uint16((hi << 8) | lo)
        return False

    def ABX(self) -> RequiresExtraCycle:
        """
        Absolute X addressing mode.

        This addressing mode uses the next two bytes as the address, then adds the X register to it.
        """
        lo = self.cpu.read(self.cpu.register.pc)
        self.cpu.register.pc += 1
        hi = self.cpu.read(self.cpu.register.pc)
        self.cpu.register.pc += 1
        self.cpu.addr_abs = uint16((hi << 8) | lo)
        self.cpu.addr_abs += self.cpu.register.x
        return (self.cpu.addr_abs & 0xFF00) != (uint16(hi) << 8)

    def ABY(self) -> RequiresExtraCycle:
        """
        Absolute Y addressing mode.

        This addressing mode uses the next two bytes as the address,
        then adds the Y register to it.
        """
        lo = self.cpu.read(self.cpu.register.pc)
        self.cpu.register.pc += 1
        hi = self.cpu.read(self.cpu.register.pc)
        self.cpu.register.pc += 1
        self.cpu.addr_abs = uint16((hi << 8) | lo)
        self.cpu.addr_abs += self.cpu.register.y
        return (self.cpu.addr_abs & 0xFF00) != (uint16(hi) << 8)

    def IND(self) -> RequiresExtraCycle:
        """
        Indirect addressing mode.

        This addressing mode uses the next two bytes as the address,
        then reads the address from that location.
        """
        ptr_lo = self.cpu.read(self.cpu.register.pc)
        self.cpu.register.pc += 1
        ptr_hi = self.cpu.read(self.cpu.register.pc)
        self.cpu.register.pc += 1
        ptr = uint16((ptr_hi << 8) | ptr_lo)

        # pylint: disable=unsupported-binary-operation
        if ptr_lo == 0x00FF:
            self.cpu.addr_abs = uint16(
                self.cpu.read(ptr & uint16(0xFF00)) << 8
            ) | uint16(self.cpu.read(ptr))
        else:
            self.cpu.addr_abs = uint16(self.cpu.read(uint16(ptr + 1)) << 8) | uint16(
                self.cpu.read(ptr)
            )
        return False
        # pylint: enable=unsupported-binary-operation

    def IZX(self):
        """
        Indexed Indirect X addressing mode.

        This addressing mode uses the next byte as the address, then adds the X register to it.
        """
        t = self.cpu.read(self.cpu.register.pc)
        self.cpu.register.pc += 1
        lo = self.cpu.read((t + self.cpu.register.x) & uint16(0x00FF))
        hi = self.cpu.read((t + self.cpu.register.x + 1) & uint16(0x00FF))
        self.cpu.addr_abs = uint16((hi << 8) | lo)
        return False

    def IZY(self):
        """
        Indirect Indexed Y addressing mode.

        This addressing mode uses the next byte as the address, then adds the Y register to it.
        """
        t = self.cpu.read(self.cpu.register.pc)
        self.cpu.register.pc += 1
        lo = self.cpu.read(uint16(t))
        hi = self.cpu.read((t + 1) & 0x00FF)
        self.cpu.addr_abs = uint16((hi << 8) | lo)
        self.cpu.addr_abs += self.cpu.register.y
        return (self.cpu.addr_abs & 0xFF00) != (uint16(hi) << 8)
