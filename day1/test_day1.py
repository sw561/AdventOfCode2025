import pytest
from day1 import main

def test_example():
    with open("day1/example") as f:
        line_list = f.read().strip().split()
        assert main(line_list) == (3, 6)
