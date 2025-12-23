#!/usr/bin/env python

import fileinput

def main(line_list):
    position = 50

    part1 = 0
    part2 = 0

    for line in line_list:
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

    return part1, part2

if __name__=="__main__":
    part1, part2 = main(fileinput.input())
    print("part1:", part1)
    print("part2:", part2)


