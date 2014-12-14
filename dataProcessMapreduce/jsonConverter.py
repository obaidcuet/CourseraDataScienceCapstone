#!/usr/bin/python
import sys

def createWordIndex(infileName, outfileName):
	import csv, json
	
	input = open(infileName, "rt") # Open the unigram file
	reader = csv.reader(input)
	
	uniGrams = {}
	for row in reader:
		word = row[0].strip()
		index = int(row[1].strip())
		uniGrams[word]=index # assigne word as key and index as value
	input.close()
	
	# write the unigram or token index in a JASON file 
	with open(outfileName, 'w') as fp:
		json.dump(uniGrams, fp)


infile = sys.argv[1]
outfile = sys.argv[2]
createWordIndex(infile,outfile)

