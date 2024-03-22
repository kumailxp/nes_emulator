"""
This module contains unit tests for the `add` function in the `main` module.
"""

import unittest
from main import add


def test_add():
    """
    Test the add function with various inputs.
    """
    assert add(2, 3) == 5
    assert add(-1, 5) == 4
    assert add(0, 0) == 0
    assert add(10, -10) == 0
    assert add(100, 200) == 300


class TestAdd(unittest.TestCase):
    """
    Test case for the add function.
    """

    def test_add_positive_numbers(self):
        """
        Test the add function with positive numbers.
        """
        result = add(2, 3)
        self.assertEqual(result, 5)

    def test_add_negative_numbers(self):
        """
        Test the add function with negative numbers.
        """
        result = add(-5, -10)
        self.assertEqual(result, -15)

    def test_add_zero(self):
        """
        Test the add function with zero.
        """
        result = add(0, 10)
        self.assertEqual(result, 10)


if __name__ == "__main__":
    unittest.main()
