#!/usr/bin/env python

import fileinput
from itertools import combinations
from collections import Counter

def distance2(c1, c2):
    return sum((c1i-c2i)**2 for c1i, c2i in zip(c1, c2))

def solve(coords, n_edges):
    n = len(coords)

    es = sorted(
        combinations(range(n), 2),
        key=lambda c: distance2(coords[c[0]], coords[c[1]])
        )

    # group_id[i] = g means that node i is in group g
    group_id = [i for i in range(n)]
    count_group0 = 1

    for ei, (i, j) in enumerate(es, start=1):
        # print("Connecting", coords[i], coords[j])
        if group_id[i] != group_id[j]:
            assign_group = group_id[i]
            connect_group = group_id[j]

            if assign_group > connect_group:
                assign_group, connect_group = connect_group, assign_group

            count_connections = 0
            for n_i in range(n):
                if group_id[n_i] == connect_group:
                    group_id[n_i] = assign_group
                    count_connections += 1

            if assign_group == 0:
                count_group0 += count_connections

            if count_group0 == n:
                part2 = coords[i][0] * coords[j][0]
                break

        if ei == n_edges:
            # Do part 1 here

            large_groups = Counter(group_id).most_common(3)
            part1 = 1
            for lg in large_groups:
                part1 *= lg[1]

    return part1, part2

if __name__=="__main__":
    
    coords = []
    for line in fileinput.input():
        coords.append(tuple(int(x) for x in line.split(',')))

    # for i, c in enumerate(coords):
    #     print(i, c)

    part1, part2 = solve(coords, n_edges=10 if len(coords) < 100 else 1000)

    print(part1)
    print(part2)
