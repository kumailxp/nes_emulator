"""
Copy-Left 2024 NES Emulator Project
"""
# pylint: disable=too-few-public-methods
import dataclasses
from numpy import uint8
from nes.address_mode import AddressingMode
from nes.opcodes import Opcodes

@dataclasses.dataclass
class Instruction:
    """
    Represents an instruction in the NES emulator.

    Attributes:
        opcode (str): The opcode of the instruction.
        operands (list): The operands of the instruction.
        addr_mode (AddressingMode): The addressing mode of the instruction.
    """

    opcode: Opcodes
    addr_mode: AddressingMode
    cycles: uint8
    size: int

    def __str__(self):
        return f"opcode: {self.opcode}, mode: {self.addr_mode}, cycles: {self.cycles}"

    def __repr__(self):
        return str(self)


class InstructionLookupTable:
    """
    A class representing a lookup table for instructions in an NES emulator.

    The lookup table maps opcode values to corresponding instructions.

    Attributes:
    - I (class): The Instruction class used for creating instruction objects.
    - A (class): The AddressingMode class used for specifying addressing modes.
    - lookup_table (dict): The dictionary representing the lookup table, where
        opcode values are keys and instruction objects are values.
    """
    # pylint: disable=line-too-long
    I = Instruction
    A = AddressingMode
    O = Opcodes
    u8 = uint8
    table = {
        0x00: I(O.BRK, A.IMM, u8(7), 1), 0x01: I(O.ORA, A.IZX, u8(6), 2), 0x02: I(O.JAM, A.IMP, u8(2), 0), 0x03: I(O.JAM, A.IMP, u8(8), 0),
        0x04: I(O.JAM, A.IMP, u8(3), 0), 0x05: I(O.ORA, A.ZP0, u8(3), 2), 0x06: I(O.ASL, A.ZP0, u8(5), 2), 0x07: I(O.JAM, A.IMP, u8(5), 0),
        0x08: I(O.PHP, A.IMP, u8(3), 1), 0x09: I(O.ORA, A.IMM, u8(2), 2), 0x0A: I(O.ASL, A.IMP, u8(2), 2), 0x0B: I(O.JAM, A.IMP, u8(2), 0),
        0x0C: I(O.JAM, A.IMP, u8(4), 0), 0x0D: I(O.ORA, A.ABS, u8(4), 3), 0x0E: I(O.ASL, A.ABS, u8(6), 3), 0x0F: I(O.JAM, A.IMP, u8(6), 0),

        0x10: I(O.BPL, A.REL, u8(2), 2), 0x11: I(O.ORA, A.IZY, u8(5), 2), 0x12: I(O.JAM, A.IMP, u8(2), 0), 0x13: I(O.JAM, A.IMP, u8(8), 0),
        0x14: I(O.JAM, A.IMP, u8(4), 0), 0x15: I(O.ORA, A.ZPX, u8(4), 2), 0x16: I(O.ASL, A.ZPX, u8(6), 2), 0x17: I(O.JAM, A.IMP, u8(6), 0),
        0x18: I(O.CLC, A.IMP, u8(2), 1), 0x19: I(O.ORA, A.ABY, u8(4), 3), 0x1A: I(O.JAM, A.IMP, u8(2), 0), 0x1B: I(O.JAM, A.IMP, u8(7), 0),
        0x1C: I(O.JAM, A.IMP, u8(4), 0), 0x1D: I(O.ORA, A.ABX, u8(4), 3), 0x1E: I(O.ASL, A.ABX, u8(7), 3), 0x1F: I(O.JAM, A.IMP, u8(7), 0),

        0x20: I(O.JSR, A.ABS, u8(6), 3), 0x21: I(O.AND, A.IZX, u8(6), 2), 0x22: I(O.JAM, A.IMP, u8(2), 0), 0x23: I(O.JAM, A.IMP, u8(8), 0),
        0x24: I(O.BIT, A.ZP0, u8(3), 2), 0x25: I(O.AND, A.ZP0, u8(3), 2), 0x26: I(O.ROL, A.ZP0, u8(5), 2), 0x27: I(O.JAM, A.IMP, u8(5), 0),
        0x28: I(O.PLP, A.IMP, u8(4), 1), 0x29: I(O.AND, A.IMM, u8(2), 2), 0x2A: I(O.ROL, A.IMP, u8(2), 1), 0x2B: I(O.JAM, A.IMP, u8(2), 0),
        0x2C: I(O.BIT, A.ABS, u8(4), 3), 0x2D: I(O.AND, A.ABS, u8(4), 3), 0x2E: I(O.ROL, A.ABS, u8(6), 3), 0x2F: I(O.JAM, A.IMP, u8(6), 0),

        0x30: I(O.BMI, A.REL, u8(2), 2), 0x31: I(O.AND, A.IZY, u8(5), 2), 0x32: I(O.JAM, A.IMP, u8(2), 0), 0x33: I(O.JAM, A.IMP, u8(8), 0),
        0x34: I(O.JAM, A.IMP, u8(4), 0), 0x35: I(O.AND, A.ZPX, u8(4), 2), 0x36: I(O.ROL, A.ZPX, u8(6), 2), 0x37: I(O.JAM, A.IMP, u8(6), 0),
        0x38: I(O.SEC, A.IMP, u8(2), 1), 0x39: I(O.AND, A.ABY, u8(4), 3), 0x3A: I(O.JAM, A.IMP, u8(2), 0), 0x3B: I(O.JAM, A.IMP, u8(7), 0),
        0x3C: I(O.JAM, A.IMP, u8(4), 0), 0x3D: I(O.AND, A.ABX, u8(4), 3), 0x3E: I(O.ROL, A.ABX, u8(7), 3), 0x3F: I(O.JAM, A.IMP, u8(7), 0),

        0x40: I(O.RTI, A.IMP, u8(6), 1), 0x41: I(O.EOR, A.IZX, u8(6), 2), 0x42: I(O.JAM, A.IMP, u8(2), 0), 0x43: I(O.JAM, A.IMP, u8(8), 0),
        0x44: I(O.JAM, A.IMP, u8(3), 0), 0x45: I(O.EOR, A.ZP0, u8(3), 2), 0x46: I(O.LSR, A.ZP0, u8(5), 2), 0x47: I(O.JAM, A.IMP, u8(5), 0),
        0x48: I(O.PHA, A.IMP, u8(3), 1), 0x49: I(O.EOR, A.IMM, u8(2), 2), 0x4A: I(O.LSR, A.IMP, u8(2), 1), 0x4B: I(O.JAM, A.IMP, u8(2), 0),
        0x4C: I(O.JMP, A.ABS, u8(3), 3), 0x4D: I(O.EOR, A.ABS, u8(4), 3), 0x4E: I(O.LSR, A.ABS, u8(6), 3), 0x4F: I(O.JAM, A.IMP, u8(6), 0),

        0x50: I(O.BVC, A.REL, u8(2), 2), 0x51: I(O.EOR, A.IZY, u8(5), 2), 0x52: I(O.JAM, A.IMP, u8(2), 0), 0x53: I(O.JAM, A.IMP, u8(8), 0),
        0x54: I(O.JAM, A.IMP, u8(4), 0), 0x55: I(O.EOR, A.ZPX, u8(4), 2), 0x56: I(O.LSR, A.ZPX, u8(6), 2), 0x57: I(O.JAM, A.IMP, u8(6), 0),
        0x58: I(O.CLI, A.IMP, u8(2), 1), 0x59: I(O.EOR, A.ABY, u8(4), 3), 0x5A: I(O.JAM, A.IMP, u8(2), 0), 0x5B: I(O.JAM, A.IMP, u8(7), 0),
        0x5C: I(O.JAM, A.IMP, u8(4), 0), 0x5D: I(O.EOR, A.ABX, u8(4), 3), 0x5E: I(O.LSR, A.ABX, u8(7), 3), 0x5F: I(O.JAM, A.IMP, u8(7), 0),

        0x60: I(O.RTS, A.IMP, u8(6), 1), 0x61: I(O.ADC, A.IZX, u8(6), 2), 0x62: I(O.JAM, A.IMP, u8(2), 0), 0x63: I(O.JAM, A.IMP, u8(8), 0),
        0x64: I(O.JAM, A.IMP, u8(3), 0), 0x65: I(O.ADC, A.ZP0, u8(3), 2), 0x66: I(O.ROR, A.ZP0, u8(5), 2), 0x67: I(O.JAM, A.IMP, u8(5), 0),
        0x68: I(O.PLA, A.IMP, u8(4), 1), 0x69: I(O.ADC, A.IMM, u8(2), 2), 0x6A: I(O.ROR, A.IMP, u8(2), 1), 0x6B: I(O.JAM, A.IMP, u8(2), 0),
        0x6C: I(O.JMP, A.IND, u8(5), 3), 0x6D: I(O.ADC, A.ABS, u8(4), 3), 0x6E: I(O.ROR, A.ABS, u8(6), 3), 0x6F: I(O.JAM, A.IMP, u8(6), 0),

        0x70: I(O.BVS, A.REL, u8(2), 2), 0x71: I(O.ADC, A.IZY, u8(5), 2), 0x72: I(O.JAM, A.IMP, u8(2), 0), 0x73: I(O.JAM, A.IMP, u8(8), 0),
        0x74: I(O.JAM, A.IMP, u8(4), 0), 0x75: I(O.ADC, A.ZPX, u8(4), 2), 0x76: I(O.ROR, A.ZPX, u8(6), 2), 0x77: I(O.JAM, A.IMP, u8(6), 0),
        0x78: I(O.SEI, A.IMP, u8(2), 1), 0x79: I(O.ADC, A.ABY, u8(4), 3), 0x7A: I(O.JAM, A.IMP, u8(2), 0), 0x7B: I(O.JAM, A.IMP, u8(7), 0),
        0x7C: I(O.JAM, A.IMP, u8(4), 0), 0x7D: I(O.ADC, A.ABX, u8(4), 3), 0x7E: I(O.ROR, A.ABX, u8(7), 3), 0x7F: I(O.JAM, A.IMP, u8(7), 0),

        0x80: I(O.JAM, A.IMP, u8(2), 0), 0x81: I(O.STA, A.IZX, u8(6), 2), 0x82: I(O.JAM, A.IMP, u8(2), 0), 0x83: I(O.JAM, A.IMP, u8(6), 0),
        0x84: I(O.STY, A.ZP0, u8(3), 2), 0x85: I(O.STA, A.ZP0, u8(3), 2), 0x86: I(O.STX, A.ZP0, u8(3), 2), 0x87: I(O.JAM, A.IMP, u8(3), 0),
        0x88: I(O.DEY, A.IMP, u8(2), 1), 0x89: I(O.JAM, A.IMP, u8(2), 0), 0x8A: I(O.TXA, A.IMP, u8(2), 1), 0x8B: I(O.JAM, A.IMP, u8(2), 0),
        0x8C: I(O.STY, A.ABS, u8(4), 3), 0x8D: I(O.STA, A.ABS, u8(4), 3), 0x8E: I(O.STX, A.ABS, u8(4), 3), 0x8F: I(O.JAM, A.IMP, u8(4), 0),

        0x90: I(O.BCC, A.REL, u8(2), 2), 0x91: I(O.STA, A.IZY, u8(6), 2), 0x92: I(O.JAM, A.IMP, u8(2), 0), 0x93: I(O.JAM, A.IMP, u8(6), 0),
        0x94: I(O.STY, A.ZPX, u8(4), 2), 0x95: I(O.STA, A.ZPX, u8(4), 2), 0x96: I(O.STX, A.ZPY, u8(4), 2), 0x97: I(O.JAM, A.IMP, u8(4), 0),
        0x98: I(O.TYA, A.IMP, u8(2), 1), 0x99: I(O.STA, A.ABY, u8(5), 3), 0x9A: I(O.TXS, A.IMP, u8(2), 1), 0x9B: I(O.JAM, A.IMP, u8(5), 0),
        0x9C: I(O.JAM, A.IMP, u8(5), 0), 0x9D: I(O.STA, A.ABX, u8(5), 3), 0x9E: I(O.JAM, A.IMP, u8(5), 0), 0x9F: I(O.JAM, A.IMP, u8(5), 0),

        0xA0: I(O.LDY, A.IMM, u8(2), 2), 0xA1: I(O.LDA, A.IZX, u8(6), 2), 0xA2: I(O.LDX, A.IMM, u8(2), 2), 0xA3: I(O.JAM, A.IMP, u8(6), 0),
        0xA4: I(O.LDY, A.ZP0, u8(3), 2), 0xA5: I(O.LDA, A.ZP0, u8(3), 2), 0xA6: I(O.LDX, A.ZP0, u8(3), 2), 0xA7: I(O.JAM, A.IMP, u8(3), 0),
        0xA8: I(O.TAY, A.IMP, u8(2), 1), 0xA9: I(O.LDA, A.IMM, u8(2), 2), 0xAA: I(O.TAX, A.IMP, u8(2), 1), 0xAB: I(O.JAM, A.IMP, u8(2), 0),
        0xAC: I(O.LDY, A.ABS, u8(4), 3), 0xAD: I(O.LDA, A.ABS, u8(4), 3), 0xAE: I(O.LDX, A.ABS, u8(4), 3), 0xAF: I(O.JAM, A.IMP, u8(4), 0),

        0xB0: I(O.BCS, A.REL, u8(2), 2), 0xB1: I(O.LDA, A.IZY, u8(5), 2), 0xB2: I(O.JAM, A.IMP, u8(2), 0), 0xB3: I(O.JAM, A.IMP, u8(5), 0),
        0xB4: I(O.LDY, A.ZPX, u8(4), 2), 0xB5: I(O.LDA, A.ZPX, u8(4), 2), 0xB6: I(O.LDX, A.ZPY, u8(4), 2), 0xB7: I(O.JAM, A.IMP, u8(4), 0),
        0xB8: I(O.CLV, A.IMP, u8(2), 1), 0xB9: I(O.LDA, A.ABY, u8(4), 3), 0xBA: I(O.TSX, A.IMP, u8(2), 1), 0xBB: I(O.JAM, A.IMP, u8(4), 0),
        0xBC: I(O.LDY, A.ABX, u8(4), 3), 0xBD: I(O.LDA, A.ABX, u8(4), 3), 0xBE: I(O.LDX, A.ABY, u8(4), 3), 0xBF: I(O.JAM, A.IMP, u8(4), 0),

        0xC0: I(O.CPY, A.IMM, u8(2), 2), 0xC1: I(O.CMP, A.IZX, u8(6), 2), 0xC2: I(O.JAM, A.IMP, u8(2), 0), 0xC3: I(O.JAM, A.IMP, u8(8), 0),
        0xC4: I(O.CPY, A.ZP0, u8(3), 2), 0xC5: I(O.CMP, A.ZP0, u8(3), 2), 0xC6: I(O.DEC, A.ZP0, u8(5), 2), 0xC7: I(O.JAM, A.IMP, u8(5), 0),
        0xC8: I(O.INY, A.IMP, u8(2), 1), 0xC9: I(O.CMP, A.IMM, u8(2), 2), 0xCA: I(O.DEX, A.IMP, u8(2), 1), 0xCB: I(O.JAM, A.IMP, u8(2), 0),
        0xCC: I(O.CPY, A.ABS, u8(4), 3), 0xCD: I(O.CMP, A.ABS, u8(4), 3), 0xCE: I(O.DEC, A.ABS, u8(6), 3), 0xCF: I(O.JAM, A.IMP, u8(6), 0),

        0xD0: I(O.BNE, A.REL, u8(2), 2), 0xD1: I(O.CMP, A.IZY, u8(5), 2), 0xD2: I(O.JAM, A.IMP, u8(2), 0), 0xD3: I(O.JAM, A.IMP, u8(8), 0),
        0xD4: I(O.JAM, A.IMP, u8(4), 0), 0xD5: I(O.CMP, A.ZPX, u8(4), 2), 0xD6: I(O.DEC, A.ZPX, u8(6), 2), 0xD7: I(O.JAM, A.IMP, u8(6), 0),
        0xD8: I(O.CLD, A.IMP, u8(2), 1), 0xD9: I(O.CMP, A.ABY, u8(4), 3), 0xDA: I(O.NOP, A.IMP, u8(2), 1), 0xDB: I(O.JAM, A.IMP, u8(7), 0),
        0xDC: I(O.JAM, A.IMP, u8(4), 0), 0xDD: I(O.CMP, A.ABX, u8(4), 3), 0xDE: I(O.DEC, A.ABX, u8(7), 3), 0xDF: I(O.JAM, A.IMP, u8(7), 0),

        0xE0: I(O.CPX, A.IMM, u8(2), 2), 0xE1: I(O.SBC, A.IZX, u8(6), 2), 0xE2: I(O.JAM, A.IMP, u8(2), 0), 0xE3: I(O.JAM, A.IMP, u8(8), 0),
        0xE4: I(O.CPX, A.ZP0, u8(3), 2), 0xE5: I(O.SBC, A.ZP0, u8(3), 2), 0xE6: I(O.INC, A.ZP0, u8(5), 2), 0xE7: I(O.JAM, A.IMP, u8(5), 0),
        0xE8: I(O.INX, A.IMP, u8(2), 1), 0xE9: I(O.SBC, A.IMM, u8(2), 2), 0xEA: I(O.NOP, A.IMP, u8(2), 1), 0xEB: I(O.JAM, A.IMP, u8(2), 0),
        0xEC: I(O.CPX, A.ABS, u8(4), 3), 0xED: I(O.SBC, A.ABS, u8(4), 3), 0xEE: I(O.INC, A.ABS, u8(6), 3), 0xEF: I(O.JAM, A.IMP, u8(6), 0),

        0xF0: I(O.BEQ, A.REL, u8(2), 2), 0xF1: I(O.SBC, A.IZY, u8(5), 2), 0xF2: I(O.JAM, A.IMP, u8(2), 0), 0xF3: I(O.JAM, A.IMP, u8(8), 0),
        0xF4: I(O.JAM, A.IMP, u8(4), 0), 0xF5: I(O.SBC, A.ZPX, u8(4), 2), 0xF6: I(O.INC, A.ZPX, u8(6), 2), 0xF7: I(O.JAM, A.IMP, u8(6), 0),
        0xF8: I(O.SED, A.IMP, u8(2), 1), 0xF9: I(O.SBC, A.ABY, u8(4), 3), 0xFA: I(O.NOP, A.IMP, u8(2), 1), 0xFB: I(O.JAM, A.IMP, u8(7), 0),
        0xFC: I(O.JAM, A.IMP, u8(4), 0), 0xFD: I(O.SBC, A.ABX, u8(4), 3), 0xFE: I(O.INC, A.ABX, u8(7), 3), 0xFF: I(O.JAM, A.IMP, u8(7), 0)
    }
    
    @staticmethod
    def opcode_lookup(opcode: uint8) -> str:
        """
        Looks up an opcode in the lookup table and returns the corresponding instruction.

        Args:
        - opcode (int): The opcode to look up.

        Returns:
        - Instruction: The instruction corresponding to the opcode.
        """
        return str(InstructionLookupTable.table[opcode].opcode)

 