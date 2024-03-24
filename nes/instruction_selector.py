"""
Implementation of the instruction selector.
"""

from numpy import uint8, uint16
from nes.olc6502 import Olc6502
from nes.flags import Flags
from nes.isa import InstructionLookupTable
from nes.address_mode import AddressingMode
from nes.opcodes import Opcodes

RequiresExtraCycle = bool


class InstructionSelector:
    """
    The InstructionSelector class is responsible for selecting and executing
    different instructions for the NES CPU (Olc6502).
    """

    def __init__(self, cpu: Olc6502):
        self.cpu = cpu

    def select(self, opcode: Opcodes) -> RequiresExtraCycle:
        """
        Selects and executes the appropriate instruction based on the given opcode.

        Args:
            opcode (Opcodes): The opcode representing the instruction to be executed.

        Returns:
            RequiresExtraCycle: The result of executing the instruction.

        Raises:
            ValueError: If the opcode is invalid.
        """
        if opcode == Opcodes.JAM:
            raise ValueError(f"Invalid opcode: {opcode}")
        return getattr(self, Opcodes(opcode).name)()

    # pylint: disable=invalid-name
    def ADC(self) -> RequiresExtraCycle:
        """
        Add with Carry.

        This instruction adds the contents of a memory location to the accumulator
        together with the carry bit. If overflow occurs, the carry bit is set, this
        enables multiple byte addition to be performed.
        """
        # Fetch the value from memory
        fetched = uint16(self.cpu.fetch())

        # Perform the addition with carry
        temp = (
            uint16(self.cpu.register.a) + fetched + uint16(self.cpu.get_flag(Flags.C))
        )

        # Set the carry flag if overflow occurs
        self.cpu.set_flag(Flags.C, bool(temp > uint16(0x00FF)))

        # Set the zero flag if the result is zero
        self.cpu.set_flag(Flags.Z, bool((temp & uint16(0x00FF)) == 0))

        # Set the negative flag if the result is negative
        self.cpu.set_flag(Flags.N, bool(temp & uint16(0x0080)))

        # Calculate the overflow flag
        a = uint16(self.cpu.register.a)
        self.cpu.set_flag(
            Flags.V, bool(uint16(~(a ^ fetched) & (a ^ temp)) & uint16(0x0080))
        )

        # Store the result in the accumulator
        self.cpu.register.a = uint8(temp & uint16(0x00FF))

        return True

    def SBC(self) -> RequiresExtraCycle:
        """
        Subtract with Carry.

        This instruction subtracts the contents of a memory location to the accumulator
        together with the carry bit. If overflow occurs, the carry bit is set, this
        enables multiple byte addition to be performed.
        """
        # Fetch the value from memory
        fetched = uint16(self.cpu.fetch())

        # Perform the subtraction with carry
        value = uint16(fetched) ^ uint16(0x00FF)
        temp = uint16(self.cpu.register.a) + value + uint16(self.cpu.get_flag(Flags.C))

        # Set the carry flag if overflow occurs
        self.cpu.set_flag(Flags.C, bool(temp & uint16(0xFF00)))

        # Set the zero flag if the result is zero
        self.cpu.set_flag(Flags.Z, bool((temp & uint16(0x00FF)) == 0))

        # Set the negative flag if the result is negative
        self.cpu.set_flag(Flags.N, bool(temp & uint16(0x0080)))

        # Calculate the overflow flag
        a = uint16(self.cpu.register.a)
        self.cpu.set_flag(
            Flags.V, bool(uint16((a ^ value) & (a ^ temp)) & uint16(0x0080))
        )

        # Store the result in the accumulator
        self.cpu.register.a = uint8(temp & uint16(0x00FF))

        return True

    def AND(self) -> RequiresExtraCycle:
        """
        Logical AND.

        This instruction performs a bitwise AND between the accumulator
        and the fetched value. The result is stored in the accumulator.
        """
        fetched = self.cpu.fetch()
        self.cpu.register.a &= fetched
        self.cpu.set_flag(Flags.Z, self.cpu.register.a == 0x00)
        self.cpu.set_flag(Flags.N, bool(self.cpu.register.a & uint8(0x80)))
        return True

    def ASL(self) -> RequiresExtraCycle:
        """
        Arithmetic Shift Left.

        This instruction shifts all bits in the accumulator or memory contents
        one position to the left. The bit that was in bit 7 is shifted into
        the carry flag. Bit 0 is set to 0.
        """
        fetched = self.cpu.fetch()
        temp = uint16(uint16(fetched) << 1)
        self.cpu.set_flag(Flags.C, bool(temp & 0xFF00))
        self.cpu.set_flag(Flags.Z, (temp & 0x00FF) == 0x00)
        self.cpu.set_flag(Flags.N, bool(temp & 0x80))

        instruction = InstructionLookupTable.table[self.cpu.opcode]
        addr_mode = instruction.addr_mode
        if addr_mode == AddressingMode.IMP:
            self.cpu.register.a = uint8(temp & 0x00FF)
        else:
            self.cpu.write(self.cpu.addr_abs, uint8(temp & 0x00FF))
        return False

    def BCC(self) -> RequiresExtraCycle:
        """
        Branch if Carry Clear.

        This instruction adds the relative displacement to the
        program counter if the carry flag is clear.
        """
        if self.cpu.get_flag(Flags.C) == 0:
            self.cpu.cycles += 1
            self.cpu.addr_abs = self.cpu.register.pc + self.cpu.addr_rel

            if (self.cpu.addr_abs & 0xFF00) != (self.cpu.register.pc & 0xFF00):
                self.cpu.cycles += 1

            self.cpu.register.pc = self.cpu.addr_abs
        return False

    def BCS(self) -> RequiresExtraCycle:
        """
        Branch if Carry Set.

        This instruction adds the relative displacement to the
        program counter if the carry flag is set.
        """
        if self.cpu.get_flag(Flags.C) == 1:
            self.cpu.cycles += 1
            self.cpu.addr_abs = self.cpu.register.pc + self.cpu.addr_rel

            if (self.cpu.addr_abs & 0xFF00) != (self.cpu.register.pc & 0xFF00):
                self.cpu.cycles += 1

            self.cpu.register.pc = self.cpu.addr_abs
        return False

    def BEQ(self) -> RequiresExtraCycle:
        """
        Branch if Equal.

        This instruction adds the relative displacement to the
        program counter if the zero flag is set.
        """
        if self.cpu.get_flag(Flags.Z) == 1:
            self.cpu.cycles += 1
            self.cpu.addr_abs = self.cpu.register.pc + self.cpu.addr_rel

            if (self.cpu.addr_abs & 0xFF00) != (self.cpu.register.pc & 0xFF00):
                self.cpu.cycles += 1

            self.cpu.register.pc = self.cpu.addr_abs
        return False

    def BIT(self) -> RequiresExtraCycle:
        """
        Bit Test.

        This instruction is used to test bits in memory with the accumulator.
        """
        fetched = self.cpu.fetch()
        temp = self.cpu.register.a & fetched
        self.cpu.set_flag(Flags.Z, temp == 0x00)
        self.cpu.set_flag(Flags.N, bool(fetched & (1 << 7)))
        self.cpu.set_flag(Flags.V, bool(fetched & (1 << 6)))
        return False

    def BMI(self) -> RequiresExtraCycle:
        """
        Branch if Minus.

        This instruction adds the relative displacement to the
        program counter if the negative flag is set.
        """
        if self.cpu.get_flag(Flags.N) == 1:
            self.cpu.cycles += 1
            self.cpu.addr_abs = self.cpu.register.pc + self.cpu.addr_rel

            if (self.cpu.addr_abs & 0xFF00) != (self.cpu.register.pc & 0xFF00):
                self.cpu.cycles += 1

            self.cpu.register.pc = self.cpu.addr_abs
        return False

    def BNE(self) -> RequiresExtraCycle:
        """
        Branch if Not Equal.

        This instruction adds the relative displacement to the
        program counter if the zero flag is clear.
        """
        if self.cpu.get_flag(Flags.Z) == 0:
            self.cpu.cycles += 1
            self.cpu.addr_abs = self.cpu.register.pc + self.cpu.addr_rel

            if (self.cpu.addr_abs & 0xFF00) != (self.cpu.register.pc & 0xFF00):
                self.cpu.cycles += 1

            self.cpu.register.pc = self.cpu.addr_abs
        return False

    def BPL(self) -> RequiresExtraCycle:
        """
        Branch if Positive.

        This instruction adds the relative displacement to the
        program counter if the negative flag is clear.
        """
        if self.cpu.get_flag(Flags.N) == 0:
            self.cpu.cycles += 1
            self.cpu.addr_abs = self.cpu.register.pc + self.cpu.addr_rel

            if (self.cpu.addr_abs & 0xFF00) != (self.cpu.register.pc & 0xFF00):
                self.cpu.cycles += 1

            self.cpu.register.pc = self.cpu.addr_abs
        return False

    def BRK(self) -> RequiresExtraCycle:
        """
        Break.

        This instruction forces the generation of an interrupt request.
        """
        self.cpu.register.pc += 1
        self.cpu.set_flag(Flags.I, True)
        self.cpu.write(
            self.cpu.register.stkp + 0x0100, (self.cpu.register.pc >> 8) & 0x00FF
        )
        self.cpu.register.stkp -= 1
        self.cpu.write(self.cpu.register.stkp + 0x0100, self.cpu.register.pc & 0x00FF)
        self.cpu.register.stkp -= 1
        self.cpu.set_flag(Flags.B, True)
        self.cpu.write(self.cpu.register.stkp, self.cpu.register.status)
        self.cpu.register.stkp -= 1
        self.cpu.set_flag(Flags.B, False)
        # pylint: disable=unsupported-binary-operation
        self.cpu.register.pc = uint16(
            uint16(self.cpu.read(uint16(0xFFFE)))
            | (uint16(uint16(self.cpu.read(uint16(0xFFFF)))) << 8)
        )
        # pylint: enable=unsupported-binary-operation
        return False

    def CLC(self) -> RequiresExtraCycle:
        """
        Clear Carry Flag.

        This instruction clears the carry flag.
        """
        self.cpu.set_flag(Flags.C, False)
        return False

    def CLD(self) -> RequiresExtraCycle:
        """
        Clear Decimal Mode.

        This instruction clears the decimal mode flag.
        """
        self.cpu.set_flag(Flags.D, False)
        return False

    def CLI(self) -> RequiresExtraCycle:
        """
        Clear Interrupt Disable.

        This instruction clears the interrupt disable flag.
        """
        self.cpu.set_flag(Flags.I, False)
        return False

    def CLV(self) -> RequiresExtraCycle:
        """
        Clear Overflow Flag.

        This instruction clears the overflow flag.
        """
        self.cpu.set_flag(Flags.V, False)
        return False

    def CMP(self) -> RequiresExtraCycle:
        """
        Compare.

        This instruction compares the contents of the accumulator with another value.
        """
        fetched = self.cpu.fetch()
        temp = uint16(self.cpu.register.a) - uint16(fetched)
        self.cpu.set_flag(Flags.C, bool(self.cpu.register.a >= fetched))
        self.cpu.set_flag(Flags.Z, bool((temp & 0x00FF) == 0x0000))
        self.cpu.set_flag(Flags.N, bool(temp & 0x0080))
        return True

    def CPX(self) -> RequiresExtraCycle:
        """
        Compare X Register.

        This instruction compares the contents of the X register with another value.
        """
        fetched = self.cpu.fetch()
        temp = uint16(self.cpu.register.x) - uint16(fetched)
        self.cpu.set_flag(Flags.C, bool(self.cpu.register.x >= fetched))
        self.cpu.set_flag(Flags.Z, bool((temp & 0x00FF) == 0x0000))
        self.cpu.set_flag(Flags.N, bool(temp & 0x0080))
        return False

    def CPY(self) -> RequiresExtraCycle:
        """
        Compare Y Register.

        This instruction compares the contents of the Y register with another value.
        """
        fetched = self.cpu.fetch()
        temp = uint16(self.cpu.register.y) - uint16(fetched)
        self.cpu.set_flag(Flags.C, bool(self.cpu.register.y >= fetched))
        self.cpu.set_flag(Flags.Z, bool((temp & 0x00FF) == 0x0000))
        self.cpu.set_flag(Flags.N, bool(temp & 0x0080))
        return False

    def DEC(self) -> RequiresExtraCycle:
        """
        Decrement Memory.

        This instruction decrements the value of a memory location.
        """
        fetched = self.cpu.fetch()
        temp = uint16(fetched) - 1
        self.cpu.write(self.cpu.addr_abs, temp & 0x00FF)
        self.cpu.set_flag(Flags.Z, bool((temp & 0x00FF) == 0x0000))
        self.cpu.set_flag(Flags.N, bool(temp & 0x0080))
        return False

    def DEX(self) -> RequiresExtraCycle:
        """
        Decrement X Register.

        This instruction decrements the value of the X register.
        """
        self.cpu.register.x -= 1
        self.cpu.set_flag(Flags.Z, bool(self.cpu.register.x == 0x00))
        self.cpu.set_flag(Flags.N, bool(self.cpu.register.x & 0x80))
        return False

    def DEY(self) -> RequiresExtraCycle:
        """
        Decrement Y Register.

        This instruction decrements the value of the Y register.
        """
        self.cpu.register.y -= 1
        self.cpu.set_flag(Flags.Z, bool(self.cpu.register.y == 0x00))
        self.cpu.set_flag(Flags.N, bool(self.cpu.register.y & 0x80))
        return False

    def EOR(self) -> RequiresExtraCycle:
        """
        Exclusive OR.

        This instruction performs a bitwise exclusive OR between the accumulator
        and the fetched value. The result is stored in the accumulator.
        """
        fetched = self.cpu.fetch()
        self.cpu.register.a ^= fetched
        self.cpu.set_flag(Flags.Z, self.cpu.register.a == 0x00)
        self.cpu.set_flag(Flags.N, bool(self.cpu.register.a & 0x80))
        return True

    def INC(self) -> RequiresExtraCycle:
        """
        Increment Memory.

        This instruction increments the value of a memory location.
        """
        fetched = self.cpu.fetch()
        temp = uint16(fetched) + 1
        self.cpu.write(self.cpu.addr_abs, temp & 0x00FF)
        self.cpu.set_flag(Flags.Z, bool((temp & 0x00FF) == 0x0000))
        self.cpu.set_flag(Flags.N, bool(temp & 0x0080))
        return False

    def INX(self) -> RequiresExtraCycle:
        """
        Increment X Register.

        This instruction increments the value of the X register.
        """
        self.cpu.register.x += 1
        self.cpu.set_flag(Flags.Z, bool(self.cpu.register.x == 0x00))
        self.cpu.set_flag(Flags.N, self.cpu.register.x & uint8(0x80))
        return False

    def INY(self) -> RequiresExtraCycle:
        """
        Increment Y Register.

        This instruction increments the value of the Y register.
        """
        self.cpu.register.y += 1
        self.cpu.set_flag(Flags.Z, bool(self.cpu.register.y == 0x00))
        self.cpu.set_flag(Flags.N, self.cpu.register.y & uint8(0x80))
        return False

    def JMP(self) -> RequiresExtraCycle:
        """
        Jump.

        This instruction sets the program counter to a new location.
        """
        self.cpu.register.pc = self.cpu.addr_abs
        return False

    def JSR(self) -> RequiresExtraCycle:
        """
        Jump to Subroutine.

        This instruction pushes the program counter minus one to the stack
        and sets the program counter to a new location.
        """
        self.cpu.register.pc -= 1
        self.cpu.write(
            0x0100 + self.cpu.register.stkp, (self.cpu.register.pc >> 8) & 0x00FF
        )
        self.cpu.register.stkp -= 1
        self.cpu.write(0x0100 + self.cpu.register.stkp, self.cpu.register.pc & 0x00FF)
        self.cpu.register.stkp -= 1
        self.cpu.register.pc = self.cpu.addr_abs
        return False

    def LDA(self) -> RequiresExtraCycle:
        """
        Load Accumulator.

        This instruction loads a value into the accumulator.
        """
        fetched = self.cpu.fetch()
        self.cpu.register.a = fetched
        self.cpu.set_flag(Flags.Z, self.cpu.register.a == 0x00)
        self.cpu.set_flag(Flags.N, bool(self.cpu.register.a & uint8(0x80)))
        return True

    def LDX(self) -> RequiresExtraCycle:
        """
        Load X Register.

        This instruction loads a value into the X register.
        """
        fetched = self.cpu.fetch()
        self.cpu.register.x = fetched
        self.cpu.set_flag(Flags.Z, self.cpu.register.x == 0x00)
        self.cpu.set_flag(Flags.N, bool(self.cpu.register.x & uint8(0x80)))
        return True

    def LDY(self) -> RequiresExtraCycle:
        """
        Load Y Register.

        This instruction loads a value into the Y register.
        """
        fetched = self.cpu.fetch()
        self.cpu.register.y = fetched
        self.cpu.set_flag(Flags.Z, self.cpu.register.y == 0x00)
        self.cpu.set_flag(Flags.N, bool(self.cpu.register.y & uint8(0x80)))
        return True

    def LSR(self) -> RequiresExtraCycle:
        """
        Logical Shift Right.

        This instruction shifts all bits in the accumulator or memory contents
        one position to the right. The bit that was in bit 0 is shifted into
        the carry flag. Bit 7 is set to 0.
        """
        fetched = uint16(self.cpu.fetch())
        self.cpu.set_flag(Flags.C, bool(fetched & 0x0001))
        temp = uint16(fetched) >> 1
        self.cpu.set_flag(Flags.Z, (temp & 0x00FF) == 0x0000)
        self.cpu.set_flag(Flags.N, bool(temp & 0x0080))
        instruction = InstructionLookupTable.table[self.cpu.opcode]
        addr_mode = instruction.addr_mode
        if addr_mode == AddressingMode.IMP:
            self.cpu.register.a = uint8(temp & 0x00FF)
        else:
            self.cpu.write(self.cpu.addr_abs, uint8(temp & 0x00FF))

        return False

    def NOP(self) -> RequiresExtraCycle:
        """
        No Operation.

        This instruction does nothing.

        Returns:
            bool: True if the instruction requires an extra cycle, False otherwise.
        """
        return self.cpu.opcode in [0x1C, 0x3C, 0x5C, 0x7C, 0xDC, 0xFC]

    def ORA(self) -> RequiresExtraCycle:
        """
        Logical OR.

        This instruction performs a bitwise OR between the accumulator
        and the fetched value. The result is stored in the accumulator.
        """
        fetched = self.cpu.fetch()
        self.cpu.register.a |= fetched
        self.cpu.set_flag(Flags.Z, self.cpu.register.a == 0x00)
        self.cpu.set_flag(Flags.N, bool(self.cpu.register.a & uint8(0x80)))
        return True

    def PHA(self) -> RequiresExtraCycle:
        """
        Push Accumulator.

        This instruction pushes the accumulator onto the stack.
        """
        self.cpu.write(0x0100 + self.cpu.register.stkp, self.cpu.register.a)
        self.cpu.register.stkp -= 1
        return False

    def PHP(self) -> RequiresExtraCycle:
        """
        Push Processor Status.

        This instruction pushes the processor status onto the stack.
        """
        self.cpu.write(
            0x0100 + self.cpu.register.stkp,
            uint8(self.cpu.register.status | Flags.B.value | Flags.U.value),
        )
        self.cpu.set_flag(Flags.B, False)
        self.cpu.set_flag(Flags.U, False)
        self.cpu.register.stkp -= 1
        return False

    def PLA(self) -> RequiresExtraCycle:
        """
        Pull Accumulator.

        This instruction pulls a value from the stack into the accumulator.
        """
        self.cpu.register.stkp += 1
        self.cpu.register.a = self.cpu.read(0x0100 + self.cpu.register.stkp)
        self.cpu.set_flag(Flags.Z, self.cpu.register.a == 0x00)
        self.cpu.set_flag(Flags.N, bool(self.cpu.register.a & uint8(0x80)))
        return False

    def PLP(self) -> RequiresExtraCycle:
        """
        Pull Processor Status.

        This instruction pulls a value from the stack into the processor status.
        """
        self.cpu.register.stkp += 1
        self.cpu.register.status = self.cpu.read(0x0100 + self.cpu.register.stkp)
        self.cpu.set_flag(Flags.U, True)
        return False

    def ROL(self) -> RequiresExtraCycle:
        """
        Rotate Left.

        This instruction rotates all bits in the accumulator or memory contents
        one position to the left. The bit that was in bit 7 is shifted into
        the carry flag. Bit 0 is set to the value of the carry flag.
        """
        fetched = uint16(self.cpu.fetch())
        temp = uint16(fetched << 1) | uint16(self.cpu.get_flag(Flags.C))
        # pylint: disable=unsupported-binary-operation
        self.cpu.set_flag(Flags.C, bool(temp & 0xFF00))
        self.cpu.set_flag(Flags.Z, (temp & 0x00FF) == 0x00)
        self.cpu.set_flag(Flags.N, bool(temp & 0x0080))
        instruction = InstructionLookupTable.table[self.cpu.opcode]
        addr_mode = instruction.addr_mode
        if addr_mode == AddressingMode.IMP:
            self.cpu.register.a = uint8(temp & 0x00FF)
        else:
            self.cpu.write(self.cpu.addr_abs, uint8(temp & 0x00FF))
        return False

    def ROR(self) -> RequiresExtraCycle:
        """
        Rotate Right.

        This instruction rotates all bits in the accumulator or memory contents
        one position to the right. The bit that was in bit 0 is shifted into
        the carry flag. Bit 7 is set to the value of the carry flag.
        """
        fetched = self.cpu.fetch()
        # pylint: disable=unsupported-binary-operation
        temp = uint16((uint16(fetched) >> 1)) | uint16(uint16(self.cpu.get_flag(Flags.C)) << 7)
        # pylint: enable=unsupported-binary-operation
        self.cpu.set_flag(Flags.C, bool(fetched & 0x01))
        self.cpu.set_flag(Flags.Z, (temp & 0x00FF) == 0x00)
        self.cpu.set_flag(Flags.N, bool(temp & 0x0080))
        instruction = InstructionLookupTable.table[self.cpu.opcode]
        addr_mode = instruction.addr_mode
        if addr_mode == AddressingMode.IMP:
            self.cpu.register.a = uint8(temp & 0x00FF)
        else:
            self.cpu.write(self.cpu.addr_abs, uint8(temp & 0x00FF))

        return False

    def RTS(self) -> RequiresExtraCycle:
        """
        Return from Subroutine.

        This instruction pulls the program counter from the stack and
        adds one to it.
        """
        self.cpu.register.stkp += 1
        self.cpu.register.pc = uint16(self.cpu.read(0x0100 + self.cpu.register.stkp))
        self.cpu.register.stkp += 1
        self.cpu.register.pc = uint16(
            uint16(self.cpu.read(0x0100 + self.cpu.register.stkp)) << 8
        )
        return False

    def SEC(self) -> RequiresExtraCycle:
        """
        Set Carry Flag.

        This instruction sets the carry flag.
        """
        self.cpu.set_flag(Flags.C, True)
        return False

    def SED(self) -> RequiresExtraCycle:
        """
        Set Decimal Mode.

        This instruction sets the decimal mode flag.
        """
        self.cpu.set_flag(Flags.D, True)
        return False

    def SEI(self) -> RequiresExtraCycle:
        """
        Set Interrupt Disable.

        This instruction sets the interrupt disable flag.
        """
        self.cpu.set_flag(Flags.I, True)
        return False

    def STA(self) -> RequiresExtraCycle:
        """
        Store Accumulator.

        This instruction stores the value of the accumulator in memory.
        """
        self.cpu.write(self.cpu.addr_abs, self.cpu.register.a)
        return False

    def STX(self) -> RequiresExtraCycle:
        """
        Store X Register.

        This instruction stores the value of the X register in memory.
        """
        self.cpu.write(self.cpu.addr_abs, self.cpu.register.x)
        return False

    def STY(self) -> RequiresExtraCycle:
        """
        Store Y Register.

        This instruction stores the value of the Y register in memory.
        """
        self.cpu.write(self.cpu.addr_abs, self.cpu.register.y)
        return False

    def TAX(self) -> RequiresExtraCycle:
        """
        Transfer Accumulator to X.

        This instruction transfers the value of the accumulator to the X register.
        """
        self.cpu.register.x = self.cpu.register.a
        self.cpu.set_flag(Flags.Z, self.cpu.register.x == 0x00)
        self.cpu.set_flag(Flags.N, bool(self.cpu.register.x & uint8(0x80)))
        return False

    def TAY(self) -> RequiresExtraCycle:
        """
        Transfer Accumulator to Y.

        This instruction transfers the value of the accumulator to the Y register.
        """
        self.cpu.register.y = self.cpu.register.a
        self.cpu.set_flag(Flags.Z, self.cpu.register.y == 0x00)
        self.cpu.set_flag(Flags.N, bool(self.cpu.register.y & uint8(0x80)))
        return False

    def TSX(self) -> RequiresExtraCycle:
        """
        Transfer Stack Pointer to X.

        This instruction transfers the value of the stack pointer to the X register.
        """
        self.cpu.register.x = self.cpu.register.stkp
        self.cpu.set_flag(Flags.Z, self.cpu.register.x == 0x00)
        self.cpu.set_flag(Flags.N, bool(self.cpu.register.x & uint8(0x80)))
        return False

    def TXA(self) -> RequiresExtraCycle:
        """
        Transfer X to Accumulator.

        This instruction transfers the value of the X register to the accumulator.
        """
        self.cpu.register.a = self.cpu.register.x
        self.cpu.set_flag(Flags.Z, self.cpu.register.a == 0x00)
        self.cpu.set_flag(Flags.N, bool(self.cpu.register.a & uint8(0x80)))
        return False

    def TXS(self) -> RequiresExtraCycle:
        """
        Transfer X to Stack Pointer.

        This instruction transfers the value of the X register to the stack pointer.
        """
        self.cpu.register.stkp = self.cpu.register.x
        return False

    def TYA(self) -> RequiresExtraCycle:
        """
        Transfer Y to Accumulator.

        This instruction transfers the value of the Y register to the accumulator.
        """
        self.cpu.register.a = self.cpu.register.y
        self.cpu.set_flag(Flags.Z, self.cpu.register.a == 0x00)
        self.cpu.set_flag(Flags.N, bool(self.cpu.register.a & uint8(0x80)))
        return False

    def RTI(self) -> RequiresExtraCycle:
        """
        Return from interrupt.

        This method is called when the processor returns from an interrupt,
        setting the program counter to the address stored on the stack.
        """
        self.cpu.register.stkp += 1
        self.cpu.register.status = self.cpu.read(0x0100 + self.cpu.register.stkp)
        self.cpu.register.status &= uint8(~Flags.B.value)
        self.cpu.register.status &= uint8(~Flags.U.value)

        self.cpu.register.stkp += 1
        self.cpu.register.pc = uint16(self.cpu.read(0x0100 + self.cpu.register.stkp))
        self.cpu.register.stkp += 1
        hi = self.cpu.read(0x0100 + self.cpu.register.stkp)
        self.cpu.register.pc |= uint16(uint16(hi) << 8)

        return False
