import pytest

from day4 import padding, count_accessible, part2

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

    s = padding([list(i) for i in s])
    assert count_accessible(s) == 13
    assert part2(s) == 43
