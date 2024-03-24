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
        0x00: I(O.BRK, A.IMM, u8(7)), 0x01: I(O.ORA, A.IZX, u8(6)), 0x02: I(O.JAM, A.IMP, u8(2)), 0x03: I(O.JAM, A.IMP, u8(8)),
        0x04: I(O.JAM, A.IMP, u8(3)), 0x05: I(O.ORA, A.ZP0, u8(3)), 0x06: I(O.ASL, A.ZP0, u8(5)), 0x07: I(O.JAM, A.IMP, u8(5)),
        0x08: I(O.PHP, A.IMP, u8(3)), 0x09: I(O.ORA, A.IMM, u8(2)), 0x0A: I(O.ASL, A.IMP, u8(2)), 0x0B: I(O.JAM, A.IMP, u8(2)),
        0x0C: I(O.JAM, A.IMP, u8(4)), 0x0D: I(O.ORA, A.ABS, u8(4)), 0x0E: I(O.ASL, A.ABS, u8(6)), 0x0F: I(O.JAM, A.IMP, u8(6)),

        0x10: I(O.BPL, A.REL, u8(2)), 0x11: I(O.ORA, A.IZY, u8(5)), 0x12: I(O.JAM, A.IMP, u8(2)), 0x13: I(O.JAM, A.IMP, u8(8)),
        0x14: I(O.JAM, A.IMP, u8(4)), 0x15: I(O.ORA, A.ZPX, u8(4)), 0x16: I(O.ASL, A.ZPX, u8(6)), 0x17: I(O.JAM, A.IMP, u8(6)),
        0x18: I(O.CLC, A.IMP, u8(2)), 0x19: I(O.ORA, A.ABY, u8(4)), 0x1A: I(O.JAM, A.IMP, u8(2)), 0x1B: I(O.JAM, A.IMP, u8(7)),
        0x1C: I(O.JAM, A.IMP, u8(4)), 0x1D: I(O.ORA, A.ABX, u8(4)), 0x1E: I(O.ASL, A.ABX, u8(7)), 0x1F: I(O.JAM, A.IMP, u8(7)),

        0x20: I(O.JSR, A.ABS, u8(6)), 0x21: I(O.AND, A.IZX, u8(6)), 0x22: I(O.JAM, A.IMP, u8(2)), 0x23: I(O.JAM, A.IMP, u8(8)),
        0x24: I(O.BIT, A.ZP0, u8(3)), 0x25: I(O.AND, A.ZP0, u8(3)), 0x26: I(O.ROL, A.ZP0, u8(5)), 0x27: I(O.JAM, A.IMP, u8(5)),
        0x28: I(O.PLP, A.IMP, u8(4)), 0x29: I(O.AND, A.IMM, u8(2)), 0x2A: I(O.ROL, A.IMP, u8(2)), 0x2B: I(O.JAM, A.IMP, u8(2)),
        0x2C: I(O.BIT, A.ABS, u8(4)), 0x2D: I(O.AND, A.ABS, u8(4)), 0x2E: I(O.ROL, A.ABS, u8(6)), 0x2F: I(O.JAM, A.IMP, u8(6)),

        0x30: I(O.BMI, A.REL, u8(2)), 0x31: I(O.AND, A.IZY, u8(5)), 0x32: I(O.JAM, A.IMP, u8(2)), 0x33: I(O.JAM, A.IMP, u8(8)),
        0x34: I(O.JAM, A.IMP, u8(4)), 0x35: I(O.AND, A.ZPX, u8(4)), 0x36: I(O.ROL, A.ZPX, u8(6)), 0x37: I(O.JAM, A.IMP, u8(6)),
        0x38: I(O.SEC, A.IMP, u8(2)), 0x39: I(O.AND, A.ABY, u8(4)), 0x3A: I(O.JAM, A.IMP, u8(2)), 0x3B: I(O.JAM, A.IMP, u8(7)),
        0x3C: I(O.JAM, A.IMP, u8(4)), 0x3D: I(O.AND, A.ABX, u8(4)), 0x3E: I(O.ROL, A.ABX, u8(7)), 0x3F: I(O.JAM, A.IMP, u8(7)),

        0x40: I(O.RTI, A.IMP, u8(6)), 0x41: I(O.EOR, A.IZX, u8(6)), 0x42: I(O.JAM, A.IMP, u8(2)), 0x43: I(O.JAM, A.IMP, u8(8)),
        0x44: I(O.JAM, A.IMP, u8(3)), 0x45: I(O.EOR, A.ZP0, u8(3)), 0x46: I(O.LSR, A.ZP0, u8(5)), 0x47: I(O.JAM, A.IMP, u8(5)),
        0x48: I(O.PHA, A.IMP, u8(3)), 0x49: I(O.EOR, A.IMM, u8(2)), 0x4A: I(O.LSR, A.IMP, u8(2)), 0x4B: I(O.JAM, A.IMP, u8(2)),
        0x4C: I(O.JMP, A.ABS, u8(3)), 0x4D: I(O.EOR, A.ABS, u8(4)), 0x4E: I(O.LSR, A.ABS, u8(6)), 0x4F: I(O.JAM, A.IMP, u8(6)),

        0x50: I(O.BVC, A.REL, u8(2)), 0x51: I(O.EOR, A.IZY, u8(5)), 0x52: I(O.JAM, A.IMP, u8(2)), 0x53: I(O.JAM, A.IMP, u8(8)),
        0x54: I(O.JAM, A.IMP, u8(4)), 0x55: I(O.EOR, A.ZPX, u8(4)), 0x56: I(O.LSR, A.ZPX, u8(6)), 0x57: I(O.JAM, A.IMP, u8(6)),
        0x58: I(O.CLI, A.IMP, u8(2)), 0x59: I(O.EOR, A.ABY, u8(4)), 0x5A: I(O.JAM, A.IMP, u8(2)), 0x5B: I(O.JAM, A.IMP, u8(7)),
        0x5C: I(O.JAM, A.IMP, u8(4)), 0x5D: I(O.EOR, A.ABX, u8(4)), 0x5E: I(O.LSR, A.ABX, u8(7)), 0x5F: I(O.JAM, A.IMP, u8(7)),

        0x60: I(O.RTS, A.IMP, u8(6)), 0x61: I(O.ADC, A.IZX, u8(6)), 0x62: I(O.JAM, A.IMP, u8(2)), 0x63: I(O.JAM, A.IMP, u8(8)),
        0x64: I(O.JAM, A.IMP, u8(3)), 0x65: I(O.ADC, A.ZP0, u8(3)), 0x66: I(O.ROR, A.ZP0, u8(5)), 0x67: I(O.JAM, A.IMP, u8(5)),
        0x68: I(O.PLA, A.IMP, u8(4)), 0x69: I(O.ADC, A.IMM, u8(2)), 0x6A: I(O.ROR, A.IMP, u8(2)), 0x6B: I(O.JAM, A.IMP, u8(2)),
        0x6C: I(O.JMP, A.IND, u8(5)), 0x6D: I(O.ADC, A.ABS, u8(4)), 0x6E: I(O.ROR, A.ABS, u8(6)), 0x6F: I(O.JAM, A.IMP, u8(6)),

        0x70: I(O.BVS, A.REL, u8(2)), 0x71: I(O.ADC, A.IZY, u8(5)), 0x72: I(O.JAM, A.IMP, u8(2)), 0x73: I(O.JAM, A.IMP, u8(8)),
        0x74: I(O.JAM, A.IMP, u8(4)), 0x75: I(O.ADC, A.ZPX, u8(4)), 0x76: I(O.ROR, A.ZPX, u8(6)), 0x77: I(O.JAM, A.IMP, u8(6)),
        0x78: I(O.SEI, A.IMP, u8(2)), 0x79: I(O.ADC, A.ABY, u8(4)), 0x7A: I(O.JAM, A.IMP, u8(2)), 0x7B: I(O.JAM, A.IMP, u8(7)),
        0x7C: I(O.JAM, A.IMP, u8(4)), 0x7D: I(O.ADC, A.ABX, u8(4)), 0x7E: I(O.ROR, A.ABX, u8(7)), 0x7F: I(O.JAM, A.IMP, u8(7)),

        0x80: I(O.JAM, A.IMP, u8(2)), 0x81: I(O.STA, A.IZX, u8(6)), 0x82: I(O.JAM, A.IMP, u8(2)), 0x83: I(O.JAM, A.IMP, u8(6)),
        0x84: I(O.STY, A.ZP0, u8(3)), 0x85: I(O.STA, A.ZP0, u8(3)), 0x86: I(O.STX, A.ZP0, u8(3)), 0x87: I(O.JAM, A.IMP, u8(3)),
        0x88: I(O.DEY, A.IMP, u8(2)), 0x89: I(O.JAM, A.IMP, u8(2)), 0x8A: I(O.TXA, A.IMP, u8(2)), 0x8B: I(O.JAM, A.IMP, u8(2)),
        0x8C: I(O.STY, A.ABS, u8(4)), 0x8D: I(O.STA, A.ABS, u8(4)), 0x8E: I(O.STX, A.ABS, u8(4)), 0x8F: I(O.JAM, A.IMP, u8(4)),

        0x90: I(O.BCC, A.REL, u8(2)), 0x91: I(O.STA, A.IZY, u8(6)), 0x92: I(O.JAM, A.IMP, u8(2)), 0x93: I(O.JAM, A.IMP, u8(6)),
        0x94: I(O.STY, A.ZPX, u8(4)), 0x95: I(O.STA, A.ZPX, u8(4)), 0x96: I(O.STX, A.ZPY, u8(4)), 0x97: I(O.JAM, A.IMP, u8(4)),
        0x98: I(O.TYA, A.IMP, u8(2)), 0x99: I(O.STA, A.ABY, u8(5)), 0x9A: I(O.TXS, A.IMP, u8(2)), 0x9B: I(O.JAM, A.IMP, u8(5)),
        0x9C: I(O.JAM, A.IMP, u8(5)), 0x9D: I(O.STA, A.ABX, u8(5)), 0x9E: I(O.JAM, A.IMP, u8(5)), 0x9F: I(O.JAM, A.IMP, u8(5)),

        0xA0: I(O.LDY, A.IMM, u8(2)), 0xA1: I(O.LDA, A.IZX, u8(6)), 0xA2: I(O.LDX, A.IMM, u8(2)), 0xA3: I(O.JAM, A.IMP, u8(6)),
        0xA4: I(O.LDY, A.ZP0, u8(3)), 0xA5: I(O.LDA, A.ZP0, u8(3)), 0xA6: I(O.LDX, A.ZP0, u8(3)), 0xA7: I(O.JAM, A.IMP, u8(3)),
        0xA8: I(O.TAY, A.IMP, u8(2)), 0xA9: I(O.LDA, A.IMM, u8(2)), 0xAA: I(O.TAX, A.IMP, u8(2)), 0xAB: I(O.JAM, A.IMP, u8(2)),
        0xAC: I(O.LDY, A.ABS, u8(4)), 0xAD: I(O.LDA, A.ABS, u8(4)), 0xAE: I(O.LDX, A.ABS, u8(4)), 0xAF: I(O.JAM, A.IMP, u8(4)),

        0xB0: I(O.BCS, A.REL, u8(2)), 0xB1: I(O.LDA, A.IZY, u8(5)), 0xB2: I(O.JAM, A.IMP, u8(2)), 0xB3: I(O.JAM, A.IMP, u8(5)),
        0xB4: I(O.LDY, A.ZPX, u8(4)), 0xB5: I(O.LDA, A.ZPX, u8(4)), 0xB6: I(O.LDX, A.ZPY, u8(4)), 0xB7: I(O.JAM, A.IMP, u8(4)),
        0xB8: I(O.CLV, A.IMP, u8(2)), 0xB9: I(O.LDA, A.ABY, u8(4)), 0xBA: I(O.TSX, A.IMP, u8(2)), 0xBB: I(O.JAM, A.IMP, u8(4)),
        0xBC: I(O.LDY, A.ABX, u8(4)), 0xBD: I(O.LDA, A.ABX, u8(4)), 0xBE: I(O.LDX, A.ABY, u8(4)), 0xBF: I(O.JAM, A.IMP, u8(4)),

        0xC0: I(O.CPY, A.IMM, u8(2)), 0xC1: I(O.CMP, A.IZX, u8(6)), 0xC2: I(O.JAM, A.IMP, u8(2)), 0xC3: I(O.JAM, A.IMP, u8(8)),
        0xC4: I(O.CPY, A.ZP0, u8(3)), 0xC5: I(O.CMP, A.ZP0, u8(3)), 0xC6: I(O.DEC, A.ZP0, u8(5)), 0xC7: I(O.JAM, A.IMP, u8(5)),
        0xC8: I(O.INY, A.IMP, u8(2)), 0xC9: I(O.CMP, A.IMM, u8(2)), 0xCA: I(O.DEX, A.IMP, u8(2)), 0xCB: I(O.JAM, A.IMP, u8(2)),
        0xCC: I(O.CPY, A.ABS, u8(4)), 0xCD: I(O.CMP, A.ABS, u8(4)), 0xCE: I(O.DEC, A.ABS, u8(6)), 0xCF: I(O.JAM, A.IMP, u8(6)),

        0xD0: I(O.BNE, A.REL, u8(2)), 0xD1: I(O.CMP, A.IZY, u8(5)), 0xD2: I(O.JAM, A.IMP, u8(2)), 0xD3: I(O.JAM, A.IMP, u8(8)),
        0xD4: I(O.JAM, A.IMP, u8(4)), 0xD5: I(O.CMP, A.ZPX, u8(4)), 0xD6: I(O.DEC, A.ZPX, u8(6)), 0xD7: I(O.JAM, A.IMP, u8(6)),
        0xD8: I(O.CLD, A.IMP, u8(2)), 0xD9: I(O.CMP, A.ABY, u8(4)), 0xDA: I(O.NOP, A.IMP, u8(2)), 0xDB: I(O.JAM, A.IMP, u8(7)),
        0xDC: I(O.JAM, A.IMP, u8(4)), 0xDD: I(O.CMP, A.ABX, u8(4)), 0xDE: I(O.DEC, A.ABX, u8(7)), 0xDF: I(O.JAM, A.IMP, u8(7)),

        0xE0: I(O.CPX, A.IMM, u8(2)), 0xE1: I(O.SBC, A.IZX, u8(6)), 0xE2: I(O.JAM, A.IMP, u8(2)), 0xE3: I(O.JAM, A.IMP, u8(8)),
        0xE4: I(O.CPX, A.ZP0, u8(3)), 0xE5: I(O.SBC, A.ZP0, u8(3)), 0xE6: I(O.INC, A.ZP0, u8(5)), 0xE7: I(O.JAM, A.IMP, u8(5)),
        0xE8: I(O.INX, A.IMP, u8(2)), 0xE9: I(O.SBC, A.IMM, u8(2)), 0xEA: I(O.NOP, A.IMP, u8(2)), 0xEB: I(O.JAM, A.IMP, u8(2)),
        0xEC: I(O.CPX, A.ABS, u8(4)), 0xED: I(O.SBC, A.ABS, u8(4)), 0xEE: I(O.INC, A.ABS, u8(6)), 0xEF: I(O.JAM, A.IMP, u8(6)),

        0xF0: I(O.BEQ, A.REL, u8(2)), 0xF1: I(O.SBC, A.IZY, u8(5)), 0xF2: I(O.JAM, A.IMP, u8(2)), 0xF3: I(O.JAM, A.IMP, u8(8)),
        0xF4: I(O.JAM, A.IMP, u8(4)), 0xF5: I(O.SBC, A.ZPX, u8(4)), 0xF6: I(O.INC, A.ZPX, u8(6)), 0xF7: I(O.JAM, A.IMP, u8(6)),
        0xF8: I(O.SED, A.IMP, u8(2)), 0xF9: I(O.SBC, A.ABY, u8(4)), 0xFA: I(O.NOP, A.IMP, u8(2)), 0xFB: I(O.JAM, A.IMP, u8(7)),
        0xFC: I(O.JAM, A.IMP, u8(4)), 0xFD: I(O.SBC, A.ABX, u8(4)), 0xFE: I(O.INC, A.ABX, u8(7)), 0xFF: I(O.JAM, A.IMP, u8(7))
    }
