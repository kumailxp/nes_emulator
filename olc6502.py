"""
This is the main file for the OLC6502 emulator.
"""

from numpy import uint8, uint16
from bus import Bus
from isa import LookupTable
from address_mode import AddressingMode
from register import Register
from flags import Flags

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
        AddressingMode.IMP: lambda _: _.imp(),
        AddressingMode.IMM: lambda _: _.imm(),
        AddressingMode.ZP0: lambda _: _.zp0(),
        AddressingMode.ZPX: lambda _: _.zpx(),
        AddressingMode.ZPY: lambda _: _.zpy(),
        AddressingMode.REL: lambda _: _.rel(),
        AddressingMode.ABS: lambda _: _.abs(),
        AddressingMode.ABX: lambda _: _.abx(),
        AddressingMode.ABY: lambda _: _.aby(),
        AddressingMode.IND: lambda _: _.ind(),
        AddressingMode.IZX: lambda _: _.izx(),
        AddressingMode.IZY: lambda _: _.izy(),
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

    def read(self, addr: uint16) -> uint8:
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

    def get_flag(self, flag: Flags):
        """
        Retrieves the value of the specified flag from the register.

        Parameters:
        - flag (Flags): The flag to retrieve.

        Returns:
        - int: The value of the specified flag.
        """
        return self.register.get_flag(flag)

    def set_flag(self, flag: Flags, value: uint8):
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
            self.opcode = self.read(self.register.pc)
            self.register.pc += 1
            instruction = LookupTable.lookup_table[self.opcode]
            self.cycles = instruction.cycles

            require_extra_cycle_from_mode = Olc6502.mode_lookup[instruction.addr_mode](
                self
            )
            require_extra_cycle_from_instruction = getattr(
                instruction, instruction.addr_mode.name.lower()
            )(self)

    def fetch(self) -> uint8:
        """
        Fetches the next instruction from memory.

        Returns:
            uint8: The fetched instruction.

        Raises:
            None

        """
        instruction = LookupTable.lookup_table[self.opcode]
        addr_mode = instruction.addr_mode
        if addr_mode != AddressingMode.IMP:
            self.fetched = self.read(self.addr_abs)
        return self.fetched

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
        self.register.pc += 1
        self.addr_abs = self.register.pc
        return False

    def zp0(self) -> RequiresExtraCycle:
        """
        Zero Page addressing mode.

        This addressing mode uses the next byte as the address.
        """
        self.addr_abs = uint16(self.read(self.register.pc))
        self.register.pc += 1
        self.addr_abs &= uint16(0x00FF)
        return False

    def zpx(self) -> RequiresExtraCycle:
        """
        Zero Page X addressing mode.

        This addressing mode uses the next byte as the address, then adds the X register to it.
        """
        self.addr_abs = uint16(self.read(self.register.pc) + self.register.x) & uint16(
            0x00FF
        )
        self.register.pc += 1
        return False

    def zpy(self) -> RequiresExtraCycle:
        """
        Zero Page Y addressing mode.

        This addressing mode uses the next byte as the address, then adds the Y register to it.
        """
        self.addr_abs = uint16(self.read(self.register.pc) + self.register.y) & uint16(
            0x00FF
        )
        self.register.pc += 1
        return False

    def rel(self) -> RequiresExtraCycle:
        """
        Relative addressing mode.

        This addressing mode uses the next byte as the address, then adds it to the program counter.
        This address mode is exclusive to branch instructions. The address must reside within
        -128 to +127 of the branch instruction, i.e. you cant directly branch to any address in
        the addressable range.
        """
        self.addr_rel = uint16(self.read(self.register.pc))
        self.register.pc += 1
        if self.addr_rel & 0x80:
            self.addr_rel |= uint16(0xFF00)
        return False

    def abs(self) -> RequiresExtraCycle:
        """
        Absolute addressing mode.

        This addressing mode uses the next two bytes as the address.
        """
        lo = self.read(self.register.pc)
        self.register.pc += 1
        hi = self.read(self.register.pc)
        self.register.pc += 1
        self.addr_abs = uint16((hi << 8) | lo)
        return False

    def abx(self) -> RequiresExtraCycle:
        """
        Absolute X addressing mode.

        This addressing mode uses the next two bytes as the address, then adds the X register to it.
        """
        lo = self.read(self.register.pc)
        self.register.pc += 1
        hi = self.read(self.register.pc)
        self.register.pc += 1
        self.addr_abs = uint16((hi << 8) | lo)
        self.addr_abs += self.register.x
        return True if (self.addr_abs & 0xFF00) != (hi << 8) else False

    def aby(self) -> RequiresExtraCycle:
        """
        Absolute Y addressing mode.

        This addressing mode uses the next two bytes as the address,
        then adds the Y register to it.
        """
        lo = self.read(self.register.pc)
        self.register.pc += 1
        hi = self.read(self.register.pc)
        self.register.pc += 1
        self.addr_abs = uint16((hi << 8) | lo)
        self.addr_abs += self.register.y
        return True if (self.addr_abs & 0xFF00) != (hi << 8) else False

    def ind(self) -> RequiresExtraCycle:
        """
        Indirect addressing mode.

        This addressing mode uses the next two bytes as the address,
        then reads the address from that location.
        """
        ptr_lo = self.read(self.register.pc)
        self.register.pc += 1
        ptr_hi = self.read(self.register.pc)
        self.register.pc += 1
        ptr = uint16((ptr_hi << 8) | ptr_lo)

        if ptr_lo == 0x00FF:
            self.addr_abs = uint16(self.read(ptr & uint16(0xFF00)) << 8) | uint16(
                self.read(ptr)
            )
        else:
            self.addr_abs = uint16(self.read(uint16(ptr + 1)) << 8) | uint16(
                self.read(ptr)
            )
        return False

    def izx(self):
        """
        Indexed Indirect X addressing mode.

        This addressing mode uses the next byte as the address, then adds the X register to it.
        """
        t = self.read(self.register.pc)
        self.register.pc += 1
        lo = self.read((t + self.register.x) & uint16(0x00FF))
        hi = self.read((t + self.register.x + 1) & uint16(0x00FF))
        self.addr_abs = uint16((hi << 8) | lo)
        return False

    def izy(self):
        """
        Indirect Indexed Y addressing mode.

        This addressing mode uses the next byte as the address, then adds the Y register to it.
        """
        t = self.read(self.register.pc)
        self.register.pc += 1
        lo = self.read(uint16(t))
        hi = self.read((t + 1) & 0x00FF)
        self.addr_abs = uint16((hi << 8) | lo)
        self.addr_abs += self.register.y
        return True if (self.addr_abs & 0xFF00) != hi << 8 else False

    # Instruction implementation for the OLC6502
    # pylint: disable=invalid-name
    def ADC(self) -> RequiresExtraCycle:
        """
        Add with Carry.

        This instruction adds the contents of a memory location to the accumulator
        together with the carry bit. If overflow occurs, the carry bit is set, this
        enables multiple byte addition to be performed.
        """
        # Fetch the value from memory
        fetched = uint16(self.fetch())

        # Perform the addition with carry
        temp = uint16(self.register.a) + fetched + uint16(self.get_flag(Flags.C))

        # Set the carry flag if overflow occurs
        self.set_flag(Flags.C, uint8(temp > uint16(0x00FF)))

        # Set the zero flag if the result is zero
        self.set_flag(Flags.Z, uint8((temp & uint16(0x00FF)) == 0))

        # Set the negative flag if the result is negative
        self.set_flag(Flags.N, uint8(temp & uint16(0x0080)))

        # Calculate the overflow flag
        a = uint16(self.register.a)
        self.set_flag(
            Flags.V, uint8(uint16(~(a ^ fetched) & (a ^ temp)) & uint16(0x0080))
        )

        # Store the result in the accumulator
        self.register.a = uint8(temp & uint16(0x00FF))

        return True

    def SBC(self) -> RequiresExtraCycle:
        """
        Subtract with Carry.

        This instruction subtracts the contents of a memory location to the accumulator
        together with the carry bit. If overflow occurs, the carry bit is set, this
        enables multiple byte addition to be performed.
        """
        # Fetch the value from memory
        fetched = uint16(self.fetch())

        # Perform the subtraction with carry
        value = uint16(fetched) ^ uint16(0x00FF)
        temp = uint16(self.register.a) + value + uint16(self.get_flag(Flags.C))

        # Set the carry flag if overflow occurs
        self.set_flag(Flags.C, uint8(temp & uint16(0xFF00)))

        # Set the zero flag if the result is zero
        self.set_flag(Flags.Z, uint8((temp & uint16(0x00FF)) == 0))

        # Set the negative flag if the result is negative
        self.set_flag(Flags.N, uint8(temp & uint16(0x0080)))

        # Calculate the overflow flag
        a = uint16(self.register.a)
        self.set_flag(Flags.V, uint8(uint16((a ^ value) & (a ^ temp)) & uint16(0x0080)))

        # Store the result in the accumulator
        self.register.a = uint8(temp & uint16(0x00FF))

        return True

    def AND(self) -> RequiresExtraCycle:
        """
        Logical AND.

        This instruction performs a bitwise AND between the accumulator
        and the fetched value. The result is stored in the accumulator.
        """
        fetched = self.fetch()
        self.register.a &= fetched
        self.set_flag(Flags.Z, self.register.a == 0x00)
        self.set_flag(Flags.N, self.register.a & uint8(0x80))
        return True

    def ASL(self) -> RequiresExtraCycle:
        """
        Arithmetic Shift Left.

        This instruction shifts all bits in the accumulator or memory contents
        one position to the left. The bit that was in bit 7 is shifted into
        the carry flag. Bit 0 is set to 0.
        """
        fetched = self.fetch()
        temp = uint16(uint16(fetched) << 1)
        self.set_flag(Flags.C, uint8(temp & 0xFF00))
        self.set_flag(Flags.Z, (temp & 0x00FF) == 0x00)
        self.set_flag(Flags.N, uint8(temp & 0x80))

        instruction = LookupTable.lookup_table[self.opcode]
        addr_mode = instruction.addr_mode
        if addr_mode == AddressingMode.IMP:
            self.register.a = uint8(temp & 0x00FF)
        else:
            self.write(self.addr_abs, uint8(temp & 0x00FF))
        return False

    def BCC(self) -> RequiresExtraCycle:
        """
        Branch if Carry Clear.

        This instruction adds the relative displacement to the
        program counter if the carry flag is clear.
        """
        if self.get_flag(Flags.C) == 0:
            self.cycles += 1
            self.addr_abs = self.register.pc + self.addr_rel

            if (self.addr_abs & 0xFF00) != (self.register.pc & 0xFF00):
                self.cycles += 1

            self.register.pc = self.addr_abs
        return False

    def BCS(self) -> RequiresExtraCycle:
        """
        Branch if Carry Set.

        This instruction adds the relative displacement to the
        program counter if the carry flag is set.
        """
        if self.get_flag(Flags.C) == 1:
            self.cycles += 1
            self.addr_abs = self.register.pc + self.addr_rel

            if (self.addr_abs & 0xFF00) != (self.register.pc & 0xFF00):
                self.cycles += 1

            self.register.pc = self.addr_abs
        return False

    def BEQ(self) -> RequiresExtraCycle:
        """
        Branch if Equal.

        This instruction adds the relative displacement to the
        program counter if the zero flag is set.
        """
        if self.get_flag(Flags.Z) == 1:
            self.cycles += 1
            self.addr_abs = self.register.pc + self.addr_rel

            if (self.addr_abs & 0xFF00) != (self.register.pc & 0xFF00):
                self.cycles += 1

            self.register.pc = self.addr_abs
        return False

    def BIT(self) -> RequiresExtraCycle:
        """
        Bit Test.

        This instruction is used to test bits in memory with the accumulator.
        """
        fetched = uint16(self.fetch())
        temp = self.register.a & fetched
        self.set_flag(Flags.Z, temp == 0x00)
        self.set_flag(Flags.N, uint8(fetched & (1 << 7)))
        self.set_flag(Flags.V, uint8(fetched & (1 << 6)))
        return False

    def BMI(self) -> RequiresExtraCycle:
        """
        Branch if Minus.

        This instruction adds the relative displacement to the
        program counter if the negative flag is set.
        """
        if self.get_flag(Flags.N) == 1:
            self.cycles += 1
            self.addr_abs = self.register.pc + self.addr_rel

            if (self.addr_abs & 0xFF00) != (self.register.pc & 0xFF00):
                self.cycles += 1

            self.register.pc = self.addr_abs
        return False

    def BNE(self) -> RequiresExtraCycle:
        """
        Branch if Not Equal.

        This instruction adds the relative displacement to the
        program counter if the zero flag is clear.
        """
        if self.get_flag(Flags.Z) == 0:
            self.cycles += 1
            self.addr_abs = self.register.pc + self.addr_rel

            if (self.addr_abs & 0xFF00) != (self.register.pc & 0xFF00):
                self.cycles += 1

            self.register.pc = self.addr_abs
        return False

    def BPL(self) -> RequiresExtraCycle:
        """
        Branch if Positive.

        This instruction adds the relative displacement to the
        program counter if the negative flag is clear.
        """
        if self.get_flag(Flags.N) == 0:
            self.cycles += 1
            self.addr_abs = self.register.pc + self.addr_rel

            if (self.addr_abs & 0xFF00) != (self.register.pc & 0xFF00):
                self.cycles += 1

            self.register.pc = self.addr_abs
        return False

    def BRK(self) -> RequiresExtraCycle:
        """
        Break.

        This instruction forces the generation of an interrupt request.
        """
        self.register.pc += 1
        self.set_flag(Flags.I, uint8(1))
        self.write(self.register.stkp + 0x0100, (self.register.pc >> 8) & 0x00FF)
        self.register.stkp -= 1
        self.write(self.register.stkp + 0x0100, self.register.pc & 0x00FF)
        self.register.stkp -= 1
        self.set_flag(Flags.B, uint8(1))
        self.write(self.register.stkp, self.register.status)
        self.register.stkp -= 1
        self.set_flag(Flags.B, uint8(0))

        self.register.pc = uint16(
            uint16(self.read(uint16(0xFFFE))) | (uint16(self.read(uint16(0xFFFF))) << 8)
        )
        return False

    def CLC(self) -> RequiresExtraCycle:
        """
        Clear Carry Flag.

        This instruction clears the carry flag.
        """
        self.set_flag(Flags.C, uint8(0))
        return False

    def CLD(self) -> RequiresExtraCycle:
        """
        Clear Decimal Mode.

        This instruction clears the decimal mode flag.
        """
        self.set_flag(Flags.D, uint8(0))
        return False

    def CLI(self) -> RequiresExtraCycle:
        """
        Clear Interrupt Disable.

        This instruction clears the interrupt disable flag.
        """
        self.set_flag(Flags.I, uint8(0))
        return False

    def CLV(self) -> RequiresExtraCycle:
        """
        Clear Overflow Flag.

        This instruction clears the overflow flag.
        """
        self.set_flag(Flags.V, uint8(0))
        return False

    def CMP(self) -> RequiresExtraCycle:
        """
        Compare.

        This instruction compares the contents of the accumulator with another value.
        """
        fetched = self.fetch()
        temp = uint16(self.register.a) - uint16(fetched)
        self.set_flag(Flags.C, uint8(self.register.a >= fetched))
        self.set_flag(Flags.Z, uint8((temp & 0x00FF) == 0x0000))
        self.set_flag(Flags.N, uint8(temp & 0x0080))
        return True

    def CPX(self) -> RequiresExtraCycle:
        """
        Compare X Register.

        This instruction compares the contents of the X register with another value.
        """
        fetched = self.fetch()
        temp = uint16(self.register.x) - uint16(fetched)
        self.set_flag(Flags.C, uint8(self.register.x >= fetched))
        self.set_flag(Flags.Z, uint8((temp & 0x00FF) == 0x0000))
        self.set_flag(Flags.N, uint8(temp & 0x0080))
        return False

    def CPY(self) -> RequiresExtraCycle:
        """
        Compare Y Register.

        This instruction compares the contents of the Y register with another value.
        """
        fetched = self.fetch()
        temp = uint16(self.register.y) - uint16(fetched)
        self.set_flag(Flags.C, uint8(self.register.y >= fetched))
        self.set_flag(Flags.Z, uint8((temp & 0x00FF) == 0x0000))
        self.set_flag(Flags.N, uint8(temp & 0x0080))
        return False

    def DEC(self) -> RequiresExtraCycle:
        """
        Decrement Memory.

        This instruction decrements the value of a memory location.
        """
        fetched = self.fetch()
        temp = uint16(fetched) - 1
        self.write(self.addr_abs, temp & 0x00FF)
        self.set_flag(Flags.Z, uint8((temp & 0x00FF) == 0x0000))
        self.set_flag(Flags.N, uint8(temp & 0x0080))
        return False

    def DEX(self) -> RequiresExtraCycle:
        """
        Decrement X Register.

        This instruction decrements the value of the X register.
        """
        self.register.x -= 1
        self.set_flag(Flags.Z, uint8(self.register.x == 0x00))
        self.set_flag(Flags.N, uint8(self.register.x & 0x80))
        return False

    def DEY(self) -> RequiresExtraCycle:
        """
        Decrement Y Register.

        This instruction decrements the value of the Y register.
        """
        self.register.y -= 1
        self.set_flag(Flags.Z, uint8(self.register.y == 0x00))
        self.set_flag(Flags.N, uint8(self.register.y & 0x80))
        return False

    def EOR(self) -> RequiresExtraCycle:
        """
        Exclusive OR.

        This instruction performs a bitwise exclusive OR between the accumulator
        and the fetched value. The result is stored in the accumulator.
        """
        fetched = self.fetch()
        self.register.a ^= fetched
        self.set_flag(Flags.Z, self.register.a == 0x00)
        self.set_flag(Flags.N, uint8(self.register.a & 0x80))
        return True

    def INC(self) -> RequiresExtraCycle:
        """
        Increment Memory.

        This instruction increments the value of a memory location.
        """
        fetched = self.fetch()
        temp = uint16(fetched) + 1
        self.write(self.addr_abs, temp & 0x00FF)
        self.set_flag(Flags.Z, uint8((temp & 0x00FF) == 0x0000))
        self.set_flag(Flags.N, uint8(temp & 0x0080))
        return False

    def INX(self) -> RequiresExtraCycle:
        """
        Increment X Register.

        This instruction increments the value of the X register.
        """
        self.register.x += 1
        self.set_flag(Flags.Z, uint8(self.register.x == 0x00))
        self.set_flag(Flags.N, self.register.x & uint8(0x80))
        return False

    def INY(self) -> RequiresExtraCycle:
        """
        Increment Y Register.

        This instruction increments the value of the Y register.
        """
        self.register.y += 1
        self.set_flag(Flags.Z, uint8(self.register.y == 0x00))
        self.set_flag(Flags.N, self.register.y & uint8(0x80))
        return False

    def JMP(self) -> RequiresExtraCycle:
        """
        Jump.

        This instruction sets the program counter to a new location.
        """
        self.register.pc = self.addr_abs
        return False

    def JSR(self) -> RequiresExtraCycle:
        """
        Jump to Subroutine.

        This instruction pushes the program counter minus one to the stack
        and sets the program counter to a new location.
        """
        self.register.pc -= 1
        self.write(0x0100 + self.register.stkp, (self.register.pc >> 8) & 0x00FF)
        self.register.stkp -= 1
        self.write(0x0100 + self.register.stkp, self.register.pc & 0x00FF)
        self.register.stkp -= 1
        self.register.pc = self.addr_abs
        return False

    def LDA(self) -> RequiresExtraCycle:
        """
        Load Accumulator.

        This instruction loads a value into the accumulator.
        """
        fetched = self.fetch()
        self.register.a = fetched
        self.set_flag(Flags.Z, self.register.a == 0x00)
        self.set_flag(Flags.N, self.register.a & uint8(0x80))
        return True

    def LDX(self) -> RequiresExtraCycle:
        """
        Load X Register.

        This instruction loads a value into the X register.
        """
        fetched = self.fetch()
        self.register.x = fetched
        self.set_flag(Flags.Z, self.register.x == 0x00)
        self.set_flag(Flags.N, self.register.x & uint8(0x80))
        return True

    def LDY(self) -> RequiresExtraCycle:
        """
        Load Y Register.

        This instruction loads a value into the Y register.
        """
        fetched = self.fetch()
        self.register.y = fetched
        self.set_flag(Flags.Z, self.register.y == 0x00)
        self.set_flag(Flags.N, self.register.y & uint8(0x80))
        return True

    def LSR(self) -> RequiresExtraCycle:
        """
        Logical Shift Right.

        This instruction shifts all bits in the accumulator or memory contents
        one position to the right. The bit that was in bit 0 is shifted into
        the carry flag. Bit 7 is set to 0.
        """
        fetched = uint16(self.fetch())
        self.set_flag(Flags.C, uint8(fetched & 0x0001))
        temp = uint16(fetched) >> 1
        self.set_flag(Flags.Z, (temp & 0x00FF) == 0x0000)
        self.set_flag(Flags.N, uint8(temp & 0x0080))
        instruction = LookupTable.lookup_table[self.opcode]
        addr_mode = instruction.addr_mode
        if addr_mode == AddressingMode.IMP:
            self.register.a = uint8(temp & 0x00FF)
        else:
            self.write(self.addr_abs, uint8(temp & 0x00FF))

        return False

    def NOP(self) -> RequiresExtraCycle:
        """
        No Operation.

        This instruction does nothing.

        Returns:
            bool: True if the instruction requires an extra cycle, False otherwise.
        """
        match self.opcode:
            case 0x1C, 0x3C, 0x5C, 0x7C, 0xDC, 0xFC:
                return True
            case _:
                return False

    def ORA(self) -> RequiresExtraCycle:
        """
        Logical OR.

        This instruction performs a bitwise OR between the accumulator
        and the fetched value. The result is stored in the accumulator.
        """
        fetched = self.fetch()
        self.register.a |= fetched
        self.set_flag(Flags.Z, self.register.a == 0x00)
        self.set_flag(Flags.N, self.register.a & uint8(0x80))
        return True

    def PHA(self) -> RequiresExtraCycle:
        """
        Push Accumulator.

        This instruction pushes the accumulator onto the stack.
        """
        self.write(0x0100 + self.register.stkp, self.register.a)
        self.register.stkp -= 1
        return False

    def PHP(self) -> RequiresExtraCycle:
        """
        Push Processor Status.

        This instruction pushes the processor status onto the stack.
        """
        self.write(
            0x0100 + self.register.stkp,
            uint8(self.register.status | Flags.B.value | Flags.U.value),
        )
        self.set_flag(Flags.B, uint8(0))
        self.set_flag(Flags.U, uint8(0))
        self.register.stkp -= 1
        return False

    def PLA(self) -> RequiresExtraCycle:
        """
        Pull Accumulator.

        This instruction pulls a value from the stack into the accumulator.
        """
        self.register.stkp += 1
        self.register.a = self.read(0x0100 + self.register.stkp)
        self.set_flag(Flags.Z, self.register.a == 0x00)
        self.set_flag(Flags.N, self.register.a & uint8(0x80))
        return False

    def PLP(self) -> RequiresExtraCycle:
        """
        Pull Processor Status.

        This instruction pulls a value from the stack into the processor status.
        """
        self.register.stkp += 1
        self.register.status = self.read(0x0100 + self.register.stkp)
        self.set_flag(Flags.U, uint8(1))
        return False

    def ROL(self) -> RequiresExtraCycle:
        """
        Rotate Left.

        This instruction rotates all bits in the accumulator or memory contents
        one position to the left. The bit that was in bit 7 is shifted into
        the carry flag. Bit 0 is set to the value of the carry flag.
        """
        fetched = self.fetch()
        temp = uint16(fetched) << 1 | self.get_flag(Flags.C)
        self.set_flag(Flags.C, uint8(temp & 0xFF00))
        self.set_flag(Flags.Z, (temp & 0x00FF) == 0x00)
        self.set_flag(Flags.N, uint8(temp & 0x0080))
        instruction = LookupTable.lookup_table[self.opcode]
        addr_mode = instruction.addr_mode
        if addr_mode == AddressingMode.IMP:
            self.register.a = uint8(temp & 0x00FF)
        else:
            self.write(self.addr_abs, uint8(temp & 0x00FF))
        return False

    def ROR(self) -> RequiresExtraCycle:
        """
        Rotate Right.

        This instruction rotates all bits in the accumulator or memory contents
        one position to the right. The bit that was in bit 0 is shifted into
        the carry flag. Bit 7 is set to the value of the carry flag.
        """
        fetched = self.fetch()
        temp = (uint16(fetched) >> 1) | uint16(self.get_flag(Flags.C) << 7)
        self.set_flag(Flags.C, uint8(fetched & 0x01))
        self.set_flag(Flags.Z, (temp & 0x00FF) == 0x00)
        self.set_flag(Flags.N, uint8(temp & 0x0080))
        instruction = LookupTable.lookup_table[self.opcode]
        addr_mode = instruction.addr_mode
        if addr_mode == AddressingMode.IMP:
            self.register.a = uint8(temp & 0x00FF)
        else:
            self.write(self.addr_abs, uint8(temp & 0x00FF))

        return False

    ### TODO: Start fixing from here
    def RTI(self) -> RequiresExtraCycle:
        """
        Return from Interrupt.

        This instruction pulls the processor status from the stack and
        sets the program counter to the address on the stack.
        """
        self.register.sp += 1
        self.register.status = self.read(self.register.sp)
        self.set_flag(Flags.B, 0)
        self.set_flag(Flags.U, 0)
        self.register.sp += 1
        self.register.pc = uint16(self.read(self.register.sp)) | (
            uint16(self.read(self.register.sp + 1)) << 8
        )
        return False

    def RTS(self) -> RequiresExtraCycle:
        """
        Return from Subroutine.

        This instruction pulls the program counter from the stack and
        adds one to it.
        """
        self.register.sp += 1
        self.register.pc = uint16(self.read(self.register.sp)) | (
            uint16(self.read(self.register.sp + 1)) << 8
        )
        self.register.pc += 1
        return False

    def SEC(self) -> RequiresExtraCycle:
        """
        Set Carry Flag.

        This instruction sets the carry flag.
        """
        self.set_flag(Flags.C, 1)
        return False

    def SED(self) -> RequiresExtraCycle:
        """
        Set Decimal Mode.

        This instruction sets the decimal mode flag.
        """
        self.set_flag(Flags.D, 1)
        return False

    def SEI(self) -> RequiresExtraCycle:
        """
        Set Interrupt Disable.

        This instruction sets the interrupt disable flag.
        """
        self.set_flag(Flags.I, 1)
        return False

    def STA(self) -> RequiresExtraCycle:
        """
        Store Accumulator.

        This instruction stores the value of the accumulator in memory.
        """
        self.write(self.addr_abs, self.register.a)
        return False

    def STX(self) -> RequiresExtraCycle:
        """
        Store X Register.

        This instruction stores the value of the X register in memory.
        """
        self.write(self.addr_abs, self.register.x)
        return False

    def STY(self) -> RequiresExtraCycle:
        """
        Store Y Register.

        This instruction stores the value of the Y register in memory.
        """
        self.write(self.addr_abs, self.register.y)
        return False

    def TAX(self) -> RequiresExtraCycle:
        """
        Transfer Accumulator to X.

        This instruction transfers the value of the accumulator to the X register.
        """
        self.register.x = self.register.a
        self.set_flag(Flags.Z, self.register.x == 0x00)
        self.set_flag(Flags.N, self.register.x & 0x80)
        return False

    def TAY(self) -> RequiresExtraCycle:
        """
        Transfer Accumulator to Y.

        This instruction transfers the value of the accumulator to the Y register.
        """
        self.register.y = self.register.a
        self.set_flag(Flags.Z, self.register.y == 0x00)
        self.set_flag(Flags.N, self.register.y & 0x80)
        return False

    def TSX(self) -> RequiresExtraCycle:
        """
        Transfer Stack Pointer to X.

        This instruction transfers the value of the stack pointer to the X register.
        """
        self.register.x = self.register.sp
        self.set_flag(Flags.Z, self.register.x == 0x00)
        self.set_flag(Flags.N, self.register.x & 0x80)
        return False

    def TXA(self) -> RequiresExtraCycle:
        """
        Transfer X to Accumulator.

        This instruction transfers the value of the X register to the accumulator.
        """
        self.register.a = self.register.x
        self.set_flag(Flags.Z, self.register.a == 0x00)
        self.set_flag(Flags.N, self.register.a & 0x80)
        return False

    def TXS(self) -> RequiresExtraCycle:
        """
        Transfer X to Stack Pointer.

        This instruction transfers the value of the X register to the stack pointer.
        """
        self.register.sp = self.register.x
        return False

    def TYA(self) -> RequiresExtraCycle:
        """
        Transfer Y to Accumulator.

        This instruction transfers the value of the Y register to the accumulator.
        """
        self.register.a = self.register.y
        self.set_flag(Flags.Z, self.register.a == 0x00)
        self.set_flag(Flags.N, self.register.a & 0x80)
        return False
