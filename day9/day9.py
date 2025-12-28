#!/usr/bin/env python

import fileinput
from itertools import combinations
import matplotlib.pyplot as plt

def area(p1, p2):
    return (abs(p1[0] - p2[0]) + 1) * (abs(p1[1] - p2[1]) + 1)

def my_range(start, end):
    d = 1 if start < end else -1
    yield from range(start, end+d, d)

def segment(p1, p2):
    if p1[0] == p2[0]:
        for y in my_range(p1[1], p2[1]):
            yield (p1[0], y)
    else:
        assert p1[1] == p2[1]
        for x in my_range(p1[0], p2[0]):
            yield (x, p1[1])

def neighbours(p):
    yield p[0]-1, p[1]
    yield p[0]+1, p[1]
    yield p[0], p[1]-1
    yield p[0], p[1]+1

def bfs(edge, start):
    points = [start]
    visited = set([start]) | edge
    while points:
        point = points.pop()
        for p in neighbours(point):
            if p in visited:
                continue
            points.append(p)
            visited.add(p)

    return visited

def solve(points):

    x_comp = sorted(set(p[0] for p in points))
    y_comp = sorted(set(p[1] for p in points))
    x_values = {x: i for i, x in enumerate(x_comp)}
    y_values = {y: i for i, y in enumerate(y_comp)}

    def compress_f(p):
        return (x_values[p[0]], y_values[p[1]])

    compressed = [compress_f(p) for p in points]

    # Construct set of all green/red points in the compressed space

    # First construct continuous perimeter list

    edge = set()
    for (p1,p2) in zip(compressed, compressed[1:] + [compressed[0]]):
        for point in segment(p1, p2):
            edge.add(point)

    # Now do bfs from (100,100) to populate all green points
    entire = bfs(edge, (2, 1) if len(points) < 10 else (100,100))

    return compress_f, entire

def valid(p1, p2, compress_f, entire):
    p1_compressed = compress_f(p1)
    p2_compressed = compress_f(p2)
    for x in my_range(p1_compressed[0], p2_compressed[0]):
        for y in my_range(p1_compressed[1], p2_compressed[1]):
            if (x,y) not in entire:
                return False
    return True

if __name__=="__main__":
    points = []
    for line in fileinput.input():
        points.append(tuple(int(x) for x in line.split(',')))

    part1 = max(
        ((p1, p2) for p1, p2 in combinations(points, 2)),
        key = lambda p1p2: area(*p1p2)
        )

    print(part1, area(*part1))

    compress_f, entire = solve(points)

    part2 = max(
        ((p1, p2) for p1, p2 in combinations(points, 2)
            if valid(p1, p2, compress_f, entire)),
        key = lambda p1p2: area(*p1p2)
        )
    print(part2, area(*part2))

    plt.plot(*zip(*points))
    plt.plot(*zip(*part1))
    plt.plot(*zip(*part2))

    plt.show()
