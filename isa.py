"""
Copy-Left 2024 NES Emulator Project
"""
import dataclasses
from address_mode import AddressingMode

@dataclasses.dataclass
class Instruction:
    """
    Represents an instruction in the NES emulator.

    Attributes:
        opcode (str): The opcode of the instruction.
        operands (list): The operands of the instruction.
        addr_mode (AddressingMode): The addressing mode of the instruction.
    """

    opcode: str
    addr_mode: AddressingMode
    cycles: int

    def __str__(self):
        return f"opcode: {self.opcode}, mode: {self.addr_mode}, cycles: {self.cycles}"

    def __repr__(self):
        return str(self)


class LookupTable:
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
    lookup_table = {
        0x00: I("BRK", A.IMM, 7), 0x01: I("ORA", A.IZX, 6), 0x02: I("???", A.IMP, 2), 0x03: I("???", A.IMP, 8),
        0x04: I("???", A.IMP, 3), 0x05: I("ORA", A.ZP0, 3), 0x06: I("ASL", A.ZP0, 5), 0x07: I("???", A.IMP, 5),
        0x08: I("PHP", A.IMP, 3), 0x09: I("ORA", A.IMM, 2), 0x0A: I("ASL", A.IMP, 2), 0x0B: I("???", A.IMP, 2),
        0x0C: I("???", A.IMP, 4), 0x0D: I("ORA", A.ABS, 4), 0x0E: I("ASL", A.ABS, 6), 0x0F: I("???", A.IMP, 6),

        0x10: I("BPL", A.REL, 2), 0x11: I("ORA", A.IZY, 5), 0x12: I("???", A.IMP, 2), 0x13: I("???", A.IMP, 8),
        0x14: I("???", A.IMP, 4), 0x15: I("ORA", A.ZPX, 4), 0x16: I("ASL", A.ZPX, 6), 0x17: I("???", A.IMP, 6),
        0x18: I("CLC", A.IMP, 2), 0x19: I("ORA", A.ABY, 4), 0x1A: I("???", A.IMP, 2), 0x1B: I("???", A.IMP, 7),
        0x1C: I("???", A.IMP, 4), 0x1D: I("ORA", A.ABX, 4), 0x1E: I("ASL", A.ABX, 7), 0x1F: I("???", A.IMP, 7),

        0x20: I("JSR", A.ABS, 6), 0x21: I("AND", A.IZX, 6), 0x22: I("???", A.IMP, 2), 0x23: I("???", A.IMP, 8),
        0x24: I("BIT", A.ZP0, 3), 0x25: I("AND", A.ZP0, 3), 0x26: I("ROL", A.ZP0, 5), 0x27: I("???", A.IMP, 5),
        0x28: I("PLP", A.IMP, 4), 0x29: I("AND", A.IMM, 2), 0x2A: I("ROL", A.IMP, 2), 0x2B: I("???", A.IMP, 2),
        0x2C: I("BIT", A.ABS, 4), 0x2D: I("AND", A.ABS, 4), 0x2E: I("ROL", A.ABS, 6), 0x2F: I("???", A.IMP, 6),

        0x30: I("BMI", A.REL, 2), 0x31: I("AND", A.IZY, 5), 0x32: I("???", A.IMP, 2), 0x33: I("???", A.IMP, 8),
        0x34: I("???", A.IMP, 4), 0x35: I("AND", A.ZPX, 4), 0x36: I("ROL", A.ZPX, 6), 0x37: I("???", A.IMP, 6),
        0x38: I("SEC", A.IMP, 2), 0x39: I("AND", A.ABY, 4), 0x3A: I("???", A.IMP, 2), 0x3B: I("???", A.IMP, 7),
        0x3C: I("???", A.IMP, 4), 0x3D: I("AND", A.ABX, 4), 0x3E: I("ROL", A.ABX, 7), 0x3F: I("???", A.IMP, 7),

        0x40: I("RTI", A.IMP, 6), 0x41: I("EOR", A.IZX, 6), 0x42: I("???", A.IMP, 2), 0x43: I("???", A.IMP, 8),
        0x44: I("???", A.IMP, 3), 0x45: I("EOR", A.ZP0, 3), 0x46: I("LSR", A.ZP0, 5), 0x47: I("???", A.IMP, 5),
        0x48: I("PHA", A.IMP, 3), 0x49: I("EOR", A.IMM, 2), 0x4A: I("LSR", A.IMP, 2), 0x4B: I("???", A.IMP, 2),
        0x4C: I("JMP", A.ABS, 3), 0x4D: I("EOR", A.ABS, 4), 0x4E: I("LSR", A.ABS, 6), 0x4F: I("???", A.IMP, 6),

        0x50: I("BVC", A.REL, 2), 0x51: I("EOR", A.IZY, 5), 0x52: I("???", A.IMP, 2), 0x53: I("???", A.IMP, 8),
        0x54: I("???", A.IMP, 4), 0x55: I("EOR", A.ZPX, 4), 0x56: I("LSR", A.ZPX, 6), 0x57: I("???", A.IMP, 6),
        0x58: I("CLI", A.IMP, 2), 0x59: I("EOR", A.ABY, 4), 0x5A: I("???", A.IMP, 2), 0x5B: I("???", A.IMP, 7),
        0x5C: I("???", A.IMP, 4), 0x5D: I("EOR", A.ABX, 4), 0x5E: I("LSR", A.ABX, 7), 0x5F: I("???", A.IMP, 7),

        0x60: I("RTS", A.IMP, 6), 0x61: I("ADC", A.IZX, 6), 0x62: I("???", A.IMP, 2), 0x63: I("???", A.IMP, 8),
        0x64: I("???", A.IMP, 3), 0x65: I("ADC", A.ZP0, 3), 0x66: I("ROR", A.ZP0, 5), 0x67: I("???", A.IMP, 5),
        0x68: I("PLA", A.IMP, 4), 0x69: I("ADC", A.IMM, 2), 0x6A: I("ROR", A.IMP, 2), 0x6B: I("???", A.IMP, 2),
        0x6C: I("JMP", A.IND, 5), 0x6D: I("ADC", A.ABS, 4), 0x6E: I("ROR", A.ABS, 6), 0x6F: I("???", A.IMP, 6),

        0x70: I("BVS", A.REL, 2), 0x71: I("ADC", A.IZY, 5), 0x72: I("???", A.IMP, 2), 0x73: I("???", A.IMP, 8),
        0x74: I("???", A.IMP, 4), 0x75: I("ADC", A.ZPX, 4), 0x76: I("ROR", A.ZPX, 6), 0x77: I("???", A.IMP, 6),
        0x78: I("SEI", A.IMP, 2), 0x79: I("ADC", A.ABY, 4), 0x7A: I("???", A.IMP, 2), 0x7B: I("???", A.IMP, 7),
        0x7C: I("???", A.IMP, 4), 0x7D: I("ADC", A.ABX, 4), 0x7E: I("ROR", A.ABX, 7), 0x7F: I("???", A.IMP, 7),

        0x80: I("???", A.IMP, 2), 0x81: I("STA", A.IZX, 6), 0x82: I("???", A.IMP, 2), 0x83: I("???", A.IMP, 6),
        0x84: I("STY", A.ZP0, 3), 0x85: I("STA", A.ZP0, 3), 0x86: I("STX", A.ZP0, 3), 0x87: I("???", A.IMP, 3),
        0x88: I("DEY", A.IMP, 2), 0x89: I("???", A.IMP, 2), 0x8A: I("TXA", A.IMP, 2), 0x8B: I("???", A.IMP, 2),
        0x8C: I("STY", A.ABS, 4), 0x8D: I("STA", A.ABS, 4), 0x8E: I("STX", A.ABS, 4), 0x8F: I("???", A.IMP, 4),

        0x90: I("BCC", A.REL, 2), 0x91: I("STA", A.IZY, 6), 0x92: I("???", A.IMP, 2), 0x93: I("???", A.IMP, 6),
        0x94: I("STY", A.ZPX, 4), 0x95: I("STA", A.ZPX, 4), 0x96: I("STX", A.ZPY, 4), 0x97: I("???", A.IMP, 4),
        0x98: I("TYA", A.IMP, 2), 0x99: I("STA", A.ABY, 5), 0x9A: I("TXS", A.IMP, 2), 0x9B: I("???", A.IMP, 5),
        0x9C: I("???", A.IMP, 5), 0x9D: I("STA", A.ABX, 5), 0x9E: I("???", A.IMP, 5), 0x9F: I("???", A.IMP, 5),

        0xA0: I("LDY", A.IMM, 2), 0xA1: I("LDA", A.IZX, 6), 0xA2: I("LDX", A.IMM, 2), 0xA3: I("???", A.IMP, 6),
        0xA4: I("LDY", A.ZP0, 3), 0xA5: I("LDA", A.ZP0, 3), 0xA6: I("LDX", A.ZP0, 3), 0xA7: I("???", A.IMP, 3),
        0xA8: I("TAY", A.IMP, 2), 0xA9: I("LDA", A.IMM, 2), 0xAA: I("TAX", A.IMP, 2), 0xAB: I("???", A.IMP, 2),
        0xAC: I("LDY", A.ABS, 4), 0xAD: I("LDA", A.ABS, 4), 0xAE: I("LDX", A.ABS, 4), 0xAF: I("???", A.IMP, 4),

        0xB0: I("BCS", A.REL, 2), 0xB1: I("LDA", A.IZY, 5), 0xB2: I("???", A.IMP, 2), 0xB3: I("???", A.IMP, 5),
        0xB4: I("LDY", A.ZPX, 4), 0xB5: I("LDA", A.ZPX, 4), 0xB6: I("LDX", A.ZPY, 4), 0xB7: I("???", A.IMP, 4),
        0xB8: I("CLV", A.IMP, 2), 0xB9: I("LDA", A.ABY, 4), 0xBA: I("TSX", A.IMP, 2), 0xBB: I("???", A.IMP, 4),
        0xBC: I("LDY", A.ABX, 4), 0xBD: I("LDA", A.ABX, 4), 0xBE: I("LDX", A.ABY, 4), 0xBF: I("???", A.IMP, 4),

        0xC0: I("CPY", A.IMM, 2), 0xC1: I("CMP", A.IZX, 6), 0xC2: I("???", A.IMP, 2), 0xC3: I("???", A.IMP, 8),
        0xC4: I("CPY", A.ZP0, 3), 0xC5: I("CMP", A.ZP0, 3), 0xC6: I("DEC", A.ZP0, 5), 0xC7: I("???", A.IMP, 5),
        0xC8: I("INY", A.IMP, 2), 0xC9: I("CMP", A.IMM, 2), 0xCA: I("DEX", A.IMP, 2), 0xCB: I("???", A.IMP, 2),
        0xCC: I("CPY", A.ABS, 4), 0xCD: I("CMP", A.ABS, 4), 0xCE: I("DEC", A.ABS, 6), 0xCF: I("???", A.IMP, 6),

        0xD0: I("BNE", A.REL, 2), 0xD1: I("CMP", A.IZY, 5), 0xD2: I("???", A.IMP, 2), 0xD3: I("???", A.IMP, 8),
        0xD4: I("???", A.IMP, 4), 0xD5: I("CMP", A.ZPX, 4), 0xD6: I("DEC", A.ZPX, 6), 0xD7: I("???", A.IMP, 6),
        0xD8: I("CLD", A.IMP, 2), 0xD9: I("CMP", A.ABY, 4), 0xDA: I("NOP", A.IMP, 2), 0xDB: I("???", A.IMP, 7),
        0xDC: I("???", A.IMP, 4), 0xDD: I("CMP", A.ABX, 4), 0xDE: I("DEC", A.ABX, 7), 0xDF: I("???", A.IMP, 7),

        0xE0: I("CPX", A.IMM, 2), 0xE1: I("SBC", A.IZX, 6), 0xE2: I("???", A.IMP, 2), 0xE3: I("???", A.IMP, 8),
        0xE4: I("CPX", A.ZP0, 3), 0xE5: I("SBC", A.ZP0, 3), 0xE6: I("INC", A.ZP0, 5), 0xE7: I("???", A.IMP, 5),
        0xE8: I("INX", A.IMP, 2), 0xE9: I("SBC", A.IMM, 2), 0xEA: I("NOP", A.IMP, 2), 0xEB: I("???", A.IMP, 2),
        0xEC: I("CPX", A.ABS, 4), 0xED: I("SBC", A.ABS, 4), 0xEE: I("INC", A.ABS, 6), 0xEF: I("???", A.IMP, 6),

        0xF0: I("BEQ", A.REL, 2), 0xF1: I("SBC", A.IZY, 5), 0xF2: I("???", A.IMP, 2), 0xF3: I("???", A.IMP, 8),
        0xF4: I("???", A.IMP, 4), 0xF5: I("SBC", A.ZPX, 4), 0xF6: I("INC", A.ZPX, 6), 0xF7: I("???", A.IMP, 6),
        0xF8: I("SED", A.IMP, 2), 0xF9: I("SBC", A.ABY, 4), 0xFA: I("NOP", A.IMP, 2), 0xFB: I("???", A.IMP, 7),
        0xFC: I("???", A.IMP, 4), 0xFD: I("SBC", A.ABX, 4), 0xFE: I("INC", A.ABX, 7), 0xFF: I("???", A.IMP, 7)
    }
