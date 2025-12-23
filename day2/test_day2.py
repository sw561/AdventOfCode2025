import pytest
from day2 import get_invalids, main

@pytest.mark.parametrize("lo, hi, e_part1, e_part2", 
    [(11, 22, 2, 2),
     (98, 115, 1, 2),
     (998, 1012, 1, 2),
     (1188511880, 1188511890, 1, 1),
     (222220, 222224, 1, 1),
     (1698522, 1698528, 0, 0),
     (446443, 446449, 1, 1),
     (38593856, 38593862, 1, 1),
     (565653, 565659, 0, 1),
     (824824821, 824824827, 0, 1),
     (2121212118, 2121212124, 0, 1)
    ])
def test_invalids(lo, hi, e_part1, e_part2):
    part1, part2 = get_invalids(lo, hi)
    assert len(part1) == e_part1
    assert len(part2) == e_part2

def test_example():
    with open("day2/example") as f:
        x = f.read()
        assert main(x) == (1227775554, 4174379265)
