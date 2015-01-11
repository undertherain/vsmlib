#!/usr/bin/env python3
import random
f = open("frequencies")
lines=f.readlines()
f.close()
N=len(lines)
for i in range (10):
    line=random.choice(lines)
    tokens=line.split()
    print (tokens[0],tokens[1])
