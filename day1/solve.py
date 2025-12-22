#!/usr/bin/env python

import fileinput

position = 50

part1 = 0
part2 = 0

for line in fileinput.input():
    d = line[0]
    x = int(line[1:])

    step = (-1 if d == "L" else 1) * x
    new_position = position + step

    if (new_position >= 100):
        part2 += (new_position // 100)
    elif new_position <= 0:
        part2 += (1 if position > 0 else 0) + (-new_position // 100)

    position = new_position % 100

    if position == 0:
        part1 += 1

print("part1:", part1)
print("part2:", part2)


