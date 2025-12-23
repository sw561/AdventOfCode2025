import pytest

from day4 import padding, count_accessible

def test_example():
    s = ["..@@.@@@@.",
         "@@@.@.@.@@",
         "@@@@@.@.@@",
         "@.@@@@..@.",
         "@@.@@@@.@@",
         ".@@@@@@@.@",
         ".@.@.@.@@@",
         "@.@@@.@@@@",
         ".@@@@@@@@.",
         "@.@.@@@.@.",
         ]

    s = padding(s)
    assert count_accessible(s) == 13
