#!/usr/bin/env python

import fileinput

def padding(s):
    ncols = len(s[0])
    padded_row = ["."] * (ncols + 2)
    ret = [padded_row]
    for row in s:
        ret.append(["."] + row + ["."])
    ret.append(padded_row)
    return ret

def accessible(s):
    accessible = []
    for i in range(len(s)):
        for j in range(len(s[i])):
            if s[i][j]!='@': continue

            count = 0
            for ii in range(i-1,i+2):
                for jj in range(j-1,j+2):
                    count += 1 if s[ii][jj] == '@' else 0

            if count <= 4:
                accessible.append((i, j))

    return accessible

def part2(s):
    total_removed = 0
    while True:
        a = accessible(s)
        if len(a) == 0: break

        for i, j in a:
            s[i][j] = '.'
            total_removed += 1

    return total_removed


def count_accessible(s):
    return len(accessible(s))

if __name__=="__main__":
    s = padding([list(line.strip()) for line in fileinput.input()])

    part1 = count_accessible(s)
    part2 = part2(s)

    print(part1)
    print(part2)
