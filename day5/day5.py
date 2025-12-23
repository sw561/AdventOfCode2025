#!/usr/bin/env python

import fileinput

def count_fresh(ranges, ids):
    fresh = set()
    for (lo,hi) in ranges:
        for i in ids:
            if lo <= i <= hi:
                fresh.add(i)
            
    return len(fresh)

def part2(ranges):
    consolidated = []
    while ranges:
        (lo, hi) = ranges.pop()
        for (l,h) in consolidated:
            if l <= lo and hi <= h:
                # Already counted. Just skip
                break
            elif lo < l and h < hi:
                ranges.append((h+1, hi))
                hi = l-1
            elif lo < l and l <= hi:
                hi = l-1
            elif lo <= h and h < hi:
                lo = h+1
            else:
                assert (h < lo or hi < l)
            assert lo <= hi
        else:
            consolidated.append((lo,hi))

    ret = sum(hi-lo+1 for (lo,hi) in consolidated)
    return ret

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
    part2 = part2(ranges)
    print("part2:", part2)
