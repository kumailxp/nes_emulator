
from main import add
import unittest
import pytest
from main import add

def test_add():
    assert add(2, 3) == 5
    assert add(-1, 5) == 4
    assert add(0, 0) == 0
    assert add(10, -10) == 0
    assert add(100, 200) == 300

class TestAdd(unittest.TestCase):
    def test_add_positive_numbers(self):
        result = add(2, 3)
        self.assertEqual(result, 5)

    def test_add_negative_numbers(self):
        result = add(-5, -10)
        self.assertEqual(result, -15)

    def test_add_zero(self):
        result = add(0, 10)
        self.assertEqual(result, 10)

if __name__ == '__main__':
    unittest.main()