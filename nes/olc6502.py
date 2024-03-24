"""
This is the main file for the OLC6502 emulator.
"""

# pylint: disable=too-many-public-methods
# pylint: disable=too-many-lines
# pylint: disable=unused-variable

import logging
from numpy import uint8, uint16
from rich.logging import RichHandler
from nes.cpu import Cpu
from nes.bus import Bus
from nes.isa import InstructionLookupTable
from nes.address_mode import AddressingMode
from nes.flags import Flags
from nes.address_mode_selector import AddressModeSelector
from nes.instruction_selector import InstructionSelector

FORMAT = "%(message)s"
logging.basicConfig(
    level="DEBUG", format=FORMAT, datefmt="[%X]", handlers=[RichHandler(level="DEBUG")]
)

log = logging.getLogger("cpu")
log.setLevel(logging.DEBUG)


class Olc6502(Cpu):
    """
    Represents the 6502 processor in the NES emulator.

    The 6502 processor is responsible for executing instructions and managing the state of the NES.

    Attributes:
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
        super().__init__()
        self.bus: Bus = bus
        self.address_mode_selector = AddressModeSelector(self)
        self.inst_selector = InstructionSelector(self)

    def read(self, addr: uint16) -> uint8:
        """
        Read data from the specified address.

        Args:
            addr: The address to read from.

        Returns:
            The data read from the address.
        """
        data: uint8 = self.bus.read(addr)
        log.info("read %s from %s", hex(data), hex(addr))
        return data

    def write(self, addr: uint16, data: uint8) -> None:
        """
        Write data to the specified address.

        Args:
            addr: The address to write to.
            data: The data to write.
        """
        log.info("write %s to %s", hex(data), hex(addr))
        self.bus.write(addr, data)

    def get_flag(self, flag: Flags) -> uint8:
        """
        Retrieves the value of the specified flag from the register.

        Parameters:
        - flag (Flags): The flag to retrieve the value of.

        Returns:
        - uint8: The value of the specified flag.
        """
        return self.register.get_flag(flag)

    def set_flag(self, flag: Flags, value: bool):
        """
        Sets the flag value of the register.

        Args:
            value: The value to set the flag to.
        """
        self.register.set_flag(flag, value)

    def clock(self):
        """
        Executes one clock cycle of the 6502 processor.

        This method is responsible for fetching the opcode, incrementing the program counter,
        and executing the instruction associated with the opcode.

        """
        if self.cycles == 0:
            self.set_flag(Flags.U, True)
            self.opcode = self.read(self.register.pc)
            self.register.pc += 1
            instruction = InstructionLookupTable.table[self.opcode]
            self.cycles = instruction.cycles

            addr_mode_selector = self.address_mode_selector
            instr_selector = self.inst_selector
            require_extra_cycle_from_mode = addr_mode_selector.select(
                instruction.addr_mode
            )
            require_extra_cycle_from_instruction = instr_selector.select(
                instruction.opcode
            )

            if require_extra_cycle_from_mode and require_extra_cycle_from_instruction:
                self.cycles += 1
            self.set_flag(Flags.U, True)

        self.cycles -= 1

    def fetch(self) -> uint8:
        """
        Fetches the next instruction from memory.

        Returns:
            uint8: The fetched instruction.

        Raises:
            None

        """
        instruction = InstructionLookupTable.table[self.opcode]
        addr_mode = instruction.addr_mode
        if addr_mode != AddressingMode.IMP:
            self.fetched = self.read(self.addr_abs)
        return self.fetched

    def reset(self) -> None:
        """
        Resets the 6502 processor.

        This method is called when the processor is reset, setting the program counter to the
        address stored at the reset vector.

        """
        self.addr_abs = uint16(0xFFFC)
        lo = self.read(self.addr_abs)
        hi = self.read(self.addr_abs + 1)
        self.register.pc = uint16(uint16(uint16(hi) << 8) | uint16(lo))

        self.register.a = uint8(0)
        self.register.x = uint8(0)
        self.register.y = uint8(0)
        self.register.stkp = uint8(0xFD)
        self.register.status = uint8(0x00 | Flags.U.value)

        self.addr_rel = uint16(0)
        self.addr_abs = uint16(0)
        self.fetched = uint8(0)

        self.cycles = uint8(8)

    def irq(self) -> None:
        """
        Executes an interrupt request.

        This method is called when an interrupt request is made, setting the program counter to the
        address stored at the interrupt vector.

        """
        if self.get_flag(Flags.I) == 0:
            self.write(
                0x0100 + self.register.stkp,
                uint8(uint16(self.register.pc >> 8) & 0x00FF),
            )
            self.register.stkp -= 1
            self.write(
                0x0100 + self.register.stkp, uint8(uint16(self.register.pc) & 0x00FF)
            )
            self.register.stkp -= 1

            self.set_flag(Flags.B, False)
            self.set_flag(Flags.U, True)
            self.set_flag(Flags.I, True)
            self.write(0x0100 + self.register.stkp, self.register.status)
            self.register.stkp -= 1

            self.addr_abs = uint16(0xFFFE)
            lo = self.read(self.addr_abs)
            hi = self.read(self.addr_abs + 1)
            self.register.pc = uint16(uint16(uint16(hi) << 8) | uint16(lo))

            self.cycles = uint8(7)

    def nmi(self) -> None:
        """
        Executes a non-maskable interrupt.

        This method is called when a non-maskable interrupt is made,
        setting the program counter to the address stored at the
        non-maskable interrupt vector.

        """
        self.write(
            0x0100 + self.register.stkp, uint8(uint16(self.register.pc >> 8) & 0x00FF)
        )
        self.register.stkp -= 1
        self.write(
            0x0100 + self.register.stkp, uint8(uint16(self.register.pc) & 0x00FF)
        )
        self.register.stkp -= 1

        self.set_flag(Flags.B, False)
        self.set_flag(Flags.U, True)
        self.set_flag(Flags.I, True)
        self.write(0x0100 + self.register.stkp, self.register.status)
        self.register.stkp -= 1

        self.addr_abs = uint16(0xFFFA)
        lo = self.read(self.addr_abs)
        hi = self.read(self.addr_abs + 1)
        self.register.pc = uint16(uint16(uint16(hi) << 8) | uint16(lo))

        self.cycles = uint8(8)
