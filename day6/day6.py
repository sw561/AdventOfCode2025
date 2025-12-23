#!/usr/bin/env python

import fileinput

def multiply(numbers):
    ret = 1
    for n in numbers:
        ret *= n
    return ret

d = {'*': multiply, '+': sum}

def part1(data, ops):
    total = 0
    for i in range(len(data[0])):
        total += d[last[i]](row[i] for row in data)
    return total

if __name__=="__main__":
    
    data = [line.strip().split() for line in fileinput.input()]

    ops = data[-1]
    data = [list(map(int, row)) for row in data[:-1]]
    
    print(part1(data, ops))

