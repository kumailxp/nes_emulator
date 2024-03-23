"""
Copy-Left 2024 NES Emulator Project
"""

import logging
import numpy as np
from rich.logging import RichHandler


FORMAT = "%(message)s"
logging.basicConfig(
    level="DEBUG", format=FORMAT, datefmt="[%X]", handlers=[RichHandler(level="DEBUG")]
)

log = logging.getLogger("rich")
log.setLevel(logging.DEBUG)


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
        self.ram = np.zeros(64 * 1024, dtype=int)

    def write(self, addr : int, data : int) -> None:
        """
        Write data to the specified address.

        Args:
            addr: The address to write to.
            data: The data to write.
        """
        if addr >= 0x0000 and addr <= 0xFFFF:
            log.info("write %s to %s", hex(data), hex(addr))
            self.ram[addr] = int(data)
        else:
            log.error("Invalid address for write: %s", hex(addr))
            raise IndexError(f"Invalid address for write: {addr}")

    def read(self, addr : int) -> int:
        """
        Read data from the specified address.

        Args:
            addr: The address to read from.

        Returns:
            The data read from the address.
        """
        if addr >= 0x0000 and addr <= 0xFFFF:
            log.info("read %s from %s", hex(self.ram[addr]), hex(addr))
            return int(self.ram[addr])
        else:
            log.error("Invalid address for read: %s", hex(addr))

        return int(0x00)
