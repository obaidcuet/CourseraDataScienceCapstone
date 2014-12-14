#!/usr/bin/python

import sys

lastNgram = None
nGramCount = 0

for line in sys.stdin:
    line = line.strip()
    nGram, count = line.split(',')
	
    count = int(count)
    # if this is the first iteration
    if not lastNgram:
        lastNgram = nGram

    # if they're the same, log it
    if nGram == lastNgram:
        nGramCount += count
    else:
        # state change (previous line was k=x, this line is k=y)
        result = [lastNgram, nGramCount]
        print(",".join(str(v) for v in result))
        lastNgram = nGram
        nGramCount = count

# this is to catch the final counts after all records have been received.		
print(",".join(str(v) for v in [lastNgram, nGramCount]))

