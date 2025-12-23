#!/usr/bin/env python

import fileinput

def count_fresh(ranges, ids):
    fresh = set()
    for (lo,hi) in ranges:
        for i in ids:
            if lo <= i <= hi:
                fresh.add(i)
            
    return len(fresh)

if __name__=="__main__":
    
    ranges = []
    ids = []
    read_ranges = True
    for line in fileinput.input():
        line = line.strip()
        if line == "":
            read_ranges = False
            continue

        if read_ranges:
            r = tuple(int(x) for x in line.split('-'))
            ranges.append(r)
        else:
            ids.append(int(line))

    part1 = count_fresh(ranges, ids)
    print("part1:", part1)
        
