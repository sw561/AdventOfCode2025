#!/usr/bin/env python

import fileinput

def max_joltage(s_orig):
    s = [int(x) for x in s_orig]

    # Prioritise early occurences
    first = max((x,-i) for i,x in enumerate(s[:-1]))
    first_index = -first[1]
    second = max(s[first_index+1:])

    ret = first[0]*10 + second
    return ret

if __name__=="__main__":
    s = sum(max_joltage(line.strip()) for line in fileinput.input())
    print(s)
