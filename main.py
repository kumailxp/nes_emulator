#!/usr/bin/env python3

"""
This is the main module of the NES emulator.
"""
from nes.bus import Bus
from nes.olc6502 import Olc6502


if __name__ == "__main__":
    with open("nes.log", "w", encoding="utf-8") as file:
        pass

    nes = Bus()
    nes.load_to_ram(0x8000, "./cc65-example/build/bin/ex1.bin")
    cpu = Olc6502(nes)
    nes.ram[0xFFFC] = 0x00
    nes.ram[0xFFFD] = 0x80
    cpu.reset()

    while True:
        cpu.clock()
        if cpu.cycles == 0:
            key = input("Enter to continue...")
            if key == "q":
                break
