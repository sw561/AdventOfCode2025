#!/usr/bin/env python

import fileinput
from itertools import combinations

def area(p1, p2):
    return abs((p1[0] - p2[0] + 1) * (p1[1] - p2[1] + 1))

if __name__=="__main__":
    points = []
    for line in fileinput.input():
        points.append(tuple(int(x) for x in line.split(',')))

    part1 = max(area(p1, p2) for p1, p2 in combinations(points, 2))

    print(part1)
