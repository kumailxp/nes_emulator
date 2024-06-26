"""
Copy-Left 2024 NES Emulator Project
"""

import numpy as np
from numpy import uint8, uint16
from nes.nes_logger import setup_logger
log = setup_logger(__name__)

class Bus:
    """
    Represents the bus in the NES emulator.

    The bus is responsible for communication between the CPU, PPU, and other components of the NES.

    Attributes:
        None

    """

    def __init__(self):
        """
        Initializes the Bus object.

        The Bus object represents the memory bus of the NES emulator. It contains a RAM array
        with a size of 64KB.

        Parameters:
            None

        Returns:
            None
        """
        self.ram = np.zeros(64 * 1024, dtype=uint8)


    def write(self, addr : uint16, data : uint8) -> None:
        """
        Write data to the specified address.

        Args:
            addr: The address to write to.
            data: The data to write.
        """
        if 0x0000 <= addr <= 0xFFFF:
            #log.info("write 0x%02X to 0x%04X", hex(data), hex(addr))
            log.info(f"write 0x{data:04X} to 0x{addr:04X}")
            self.ram[addr] = int(data)
        else:
            log.error("Invalid address for write: 0x%04X", hex(addr))
            raise IndexError(f"Invalid address for write: {addr:04X}")

    def read(self, addr : uint16) -> uint8:
        """
        Read data from the specified address.

        Args:
            addr: The address to read from.

        Returns:
            The data read from the address.
        """
        if 0x0000 <= addr <= 0xFFFF:
            log.info("read 0x%02X from 0x%04X", self.ram[addr], addr)
            return uint8(self.ram[addr])

        log.error("Invalid address for read: 0x%04X", hex(addr))
        return uint8(0x00)

    def load_to_ram(self, ram_offset: int, game_file: str) -> int:
        """
        Loads the contents of a game file into the RAM of the NES emulator.

        Args:
            ram_offset (int): The starting offset in the RAM where the data should be loaded.
            game_file (str): The path to the game file.

        """
        with open(game_file, 'rb') as f:
            data = f.read()
            data_list = list(data)
            for data in data_list:
                self.ram[ram_offset] = data
                ram_offset += 1
        return ram_offset
