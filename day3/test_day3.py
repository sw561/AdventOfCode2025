import pytest
from day3 import max_joltage

@pytest.mark.parametrize("s, expected", 
    [("987654321111111", 98),
     ("811111111111119", 89),
     ("234234234234278", 78),
     ("818181911112111", 92),
    ])
def test_invalids(s, expected):
    assert max_joltage(s) == expected
