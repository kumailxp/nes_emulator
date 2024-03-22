#!/usr/bin/env python3

"""
This is the main module of the NES emulator.

It contains the `add` function which adds two numbers and returns the result.

Usage:
    To use this module, import it and call the `add` function with two numbers as arguments.

Example:
    >>> add(2, 3)
    5
"""


from rich import print as rprint

def add(a, b):
    """
    Adds two numbers and returns the result.

    Parameters:
    a (int): The first number.
    b (int): The second number.

    Returns:
    int: The sum of the two numbers.
    """
    return a + b


if __name__ == "__main__":
    rprint("[bold red]hello")
    print(add(2, 3))
