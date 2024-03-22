""" 
Tests for the Bus class.
"""
import unittest
from bus import Bus

class TestBus(unittest.TestCase):
    """
    Test case for the Bus class.
    """

    def test_write_valid_address(self):
        """
        Test writing data to a valid address.
        """
        bus = Bus()
        bus.write(0x1234, 0xAB)
        self.assertEqual(bus.ram[0x1234], 0xAB)

    def test_write_invalid_address(self):
        """
        Test writing data to an invalid address.
        """
        bus = Bus()
        with self.assertRaises(IndexError):
            bus.write(0xFFFFF, 0xCD)

    def test_write_data(self):
        """
        Test writing different data values.
        """
        bus = Bus()
        bus.write(0x2000, 0x55)
        self.assertEqual(bus.ram[0x2000], 0x55)

        bus.write(0x3000, 0xAA)
        self.assertEqual(bus.ram[0x3000], 0xAA)

        bus.write(0x4000, 0xFF)
        self.assertEqual(bus.ram[0x4000], 0xFF)

    def test_read_valid_address(self):
        """
        Test reading data from a valid address.
        """
        bus = Bus()
        bus.ram[0x5678] = 0x12
        result = bus.read(0x5678)
        self.assertEqual(result, 0x12)

    def test_read_invalid_address(self):
        """
        Test reading data from an invalid address.
        """
        bus = Bus()
        result = bus.read(0xFFFFF)
        self.assertEqual(result, 0x00)

    def test_read_data(self):
        """
        Test reading data from different addresses.
        """
        bus = Bus()
        bus.ram[0x1000] = 0x34
        result = bus.read(0x1000)
        self.assertEqual(result, 0x34)

        bus.ram[0x2000] = 0x56
        result = bus.read(0x2000)
        self.assertEqual(result, 0x56)

        bus.ram[0x3000] = 0x78
        result = bus.read(0x3000)
        self.assertEqual(result, 0x78)

if __name__ == '__main__':
    unittest.main()
