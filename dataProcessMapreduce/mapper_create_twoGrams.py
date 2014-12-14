#!/usr/bin/python

import sys, re

def listProfanity(infileName):
	import csv
	input = open(infileName, "rt")
	reader = csv.reader(input)
	profanity = []
	for row in reader:
		word = row
		profanity.extend(word)
	input.close()
	return profanity

## replace all except alphabets and apostrophe
def numPuntuationCleaner(inputStr):
    # below steps should be done in sequence as here
	
	# 1.replace all back tick with single quote
	inputStr = re.sub(r"`", "'", inputStr)

	# 2.replace all except single quote & words 
	inputStr = re.sub(r"[^\w' ]", "", inputStr)
	
	# 3.replace all under score "_" with space
	inputStr = re.sub(r"[_]", " ", inputStr)
	
	# 4.replace all single quotes except apostrophe s,t,d & ve.
	# This should be done after replace all except single quote & words 
	inputStr = re.sub(r"(?!'[stdm] |'ve |'re )'", " ", inputStr)
	
	# 5. Replace all standalone numbers and numbers that are start of word
	inputStr = re.sub("^\d+| \d+|\t+\d+", " ", inputStr)
	
	# 6. Replace extra spaces and tabs with single spaces
	inputStr=re.sub(r" +|\t+", " ", inputStr)

	# 7. Repace starting and trailing spaces and tabs
	out=re.sub(r"^ +| +$|^\t+|\t+$", "", inputStr)
	
	return out

def profinatyWordsCleaner(input, inprofinatyWords):
	remove = '|'.join(inprofinatyWords)
	regex = re.compile(r"\b"+remove+"\b", flags=re.IGNORECASE)
	out=' '.join(regex.sub("", input).split())
	return out

def ngrams(input, n):
	input = input.split(' ')
	output = {}
	for i in range(len(input)-n+1):
		g = ' '.join(input[i:i+n])
		output.setdefault(g, 0)
		output[g] += 1
	return output

	
###______________main________________________
# only put filename, not full path. add full path in -file/-files parameter of hadoop strems
profanityFile = "profanity_words.txt"
profinatyWords = listProfanity(profanityFile)

for line in sys.stdin:
	listSentence = re.split("\.|\?|!|,",line) # seperate sentences in the line seperated by ".!?"
	for sentence in listSentence:
		if len(sentence.strip()) > 0:
			# Clean all profanity words
			sentence = profinatyWordsCleaner(sentence, profinatyWords)
			
			# Clean all extra symbols and standalone numbers
			# This should be called after profinaty cleaning to avoid extra spaces
			sentence = numPuntuationCleaner(sentence) 
								
			# claculate ngram from current line
			biGrams = ngrams(sentence,2)
			
			# emitting ngrams to stdout
			for key, value in biGrams.items():
				print(key+","+str(value))




