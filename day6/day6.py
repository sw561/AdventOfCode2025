#!/usr/bin/env python

import fileinput

def multiply(numbers):
    ret = 1
    for n in numbers:
        ret *= n
    return ret

d = {'*': multiply, '+': sum}

def part1(data, ops):
    ops = ops.split()
    data = [list(map(int, row.split())) for row in data]

    total = 0
    for i in range(len(data[0])):
        total += d[ops[i]](row[i] for row in data)
    return total

def get_edges(ops):
    for i in range(len(ops)):
        if ops[i] != ' ':
            yield i
    yield len(ops)+1

def drop_one(g):
    next(g)
    yield from g

def build_int(digits):
    ret = 0
    for d in digits:
        if d == ' ': continue
        ret = ret * 10 + int(d)
    return ret

def part2(data, ops):
    total = 0
    for start, end in zip(get_edges(ops), drop_one(get_edges(ops))):
        total += d[ops[start]](
            (build_int(row[index] for row in data))
                for index in range(start, end-1)
            )

    return total

if __name__=="__main__":
    
    data = [line.strip('\n') for line in fileinput.input()]
    
    ops = data[-1]
    data = data[:-1]

    print(part1(data, ops))
    print(part2(data, ops))

