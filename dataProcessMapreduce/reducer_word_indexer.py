#!/usr/bin/python

import sys

index = 0
for line in sys.stdin:
	word,freq = line.split(",")
	index = index + 1
	print(word+","+str(index))



