import pytest
from day3 import max_joltage

@pytest.mark.parametrize("s, p1, p2", 
    [("987654321111111", 98, 987654321111),
     ("811111111111119", 89, 811111111119),
     ("234234234234278", 78, 434234234278),
     ("818181911112111", 92, 888911112111),
    ])
def test_joltage(s, p1, p2):
    s = [int(x) for x in s]
    assert max_joltage(s) == p1
    assert max_joltage(s, n=12) == p2
