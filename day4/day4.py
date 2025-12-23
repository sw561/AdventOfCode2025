#!/usr/bin/env python

import fileinput

def padding(s):
    ncols = len(s[0])
    padded_row = "." * (ncols + 2)
    ret = [padded_row]
    for row in s:
        ret.append("." + row + ".")
    ret.append(padded_row)
    return ret

def count_accessible(s):
    accessible = 0
    for i in range(len(s)):
        for j in range(len(s[i])):
            if s[i][j]!='@': continue

            count = 0
            for ii in range(i-1,i+2):
                for jj in range(j-1,j+2):
                    count += 1 if s[ii][jj] == '@' else 0

            accessible += 1 if count <= 4 else 0

    return accessible

if __name__=="__main__":
    s = padding([line.strip() for line in fileinput.input()])

    part1 = count_accessible(s)

    print(part1)
