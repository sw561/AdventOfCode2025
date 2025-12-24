#!/usr/bin/env python

import fileinput

def simulate(data):
    splits = 0

    beams = set()

    for i, x in enumerate(data[0]):
        if x == "S":
            beams.add(i)
            break

    for row in data[1:]:

        new_beams = set()
        for b in beams:
            if row[b] == '.':
                new_beams.add(b)
            elif row[b] == '^':
                new_beams.add(b-1)
                new_beams.add(b+1)
                splits += 1

        beams = new_beams

    return splits

if __name__=="__main__":
    data = [line.strip() for line in fileinput.input()]

    print(simulate(data))
