#!/usr/bin/env python

import fileinput
from collections import defaultdict

def simulate(data):
    splits = 0

    beams = dict() # for each position, beams[position] is number of worlds

    for i, x in enumerate(data[0]):
        if x == "S":
            beams[i] = 1
            break

    for row in data[1:]:

        new_beams = defaultdict(lambda: 0)
        for b, n in beams.items():
            if row[b] == '.':
                new_beams[b] += n
            elif row[b] == '^':
                new_beams[b-1] += n
                new_beams[b+1] += n
                splits += 1

        beams = new_beams

    return splits, sum(beams.values())

if __name__=="__main__":
    data = [line.strip() for line in fileinput.input()]

    print(simulate(data))
