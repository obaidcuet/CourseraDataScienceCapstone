#!/usr/bin/python
import sys

def readWordIndex(infileName):
	import json
	with open(infileName, 'r') as fp:
		wordIndex = json.load(fp)
	return wordIndex # retrun as distionaly

##__________________main__________________
jsonFile = "wordidx.json"
wordIndex = readWordIndex(jsonFile)

for line in sys.stdin:
	bigram,freq = line.strip().split(",")
	#print(bigram+"|"+freq)
	words = bigram.split(" ")
	index1 = wordIndex.get(words[0])
	index2 = wordIndex.get(words[1])
	print(str(freq)+","+words[0]+","+str(index1)+","+","+words[0]+str(index2))
	
	#print(str(freq)+","+str(index1)+","+str(index2))


