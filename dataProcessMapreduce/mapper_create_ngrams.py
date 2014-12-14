# /tmp/corpus/input
# /tmp/corpus/ngrams
# /tmp/corpus/finalindexedngrams

import os, sys, re, csv

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
	inputStr = re.sub(r"(?!'[stdm]|'ve|'re)'", " ", inputStr)
	
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

basePath = "/stage/AIU/corpus"
profanityFile = basePath+"/profanity_words.txt"
profinatyWords = listProfanity(profanityFile)

#inputPath = basePath+"/input"
#outPath = basePath+"/n-grams"

# Open files where n grams will be written
#uniGramWriter = open(outPath+'/uniGram.csv', 'wt')
#biGramWriter = open(outPath+'/biGram.csv', 'wt')
#triGramWriter = open(outPath+'/triGram.csv', 'wt')
#quadGramWriter = open(outPath+'/quadGram.csv', 'wt')

# List input text files in the input directory
dirs = os.listdir(inputPath)

for fileName in dirs:
	with open(inputPath+"/"+fileName, "rt") as f:
		for line in f:
			listSentence = re.split("\.|\?|!|,",line) # seperate sentences in the line seperated by ".!?"
			for sentence in listSentence:
				if len(sentence.strip()) > 0:
					# Clean all profanity words
					sentence = profinatyWordsCleaner(sentence, profinatyWords)
					
					# Clean all extra symbols and standalone numbers
					# This should be called after profinaty cleaning to avoid extra spaces
					sentence = numPuntuationCleaner(sentence) 
										
					# Writing n-grams to file
					uniGrams = ngrams(sentence,1)
					for key, value in uniGrams.items():
					#if len(key.strip()) > 0:
						uniGramWriter.write("\""+key+"\","+str(value)+"\n")
											
					biGrams = ngrams(sentence,2)
					for key, value in biGrams.items():
						#if len(key.strip()) > 0:
						biGramWriter.write("\""+key+"\","+str(value)+"\n")
					
					triGrams = ngrams(sentence,3)
					for key, value in triGrams.items():
						#if len(key.strip()) > 0:
						triGramWriter.write("\""+key+"\","+str(value)+"\n")
					
					quadGrams = ngrams(sentence,4)
					for key, value in quadGrams.items():
						#if len(key.strip()) > 0:
						quadGramWriter.write("\""+key+"\","+str(value)+"\n")

# Close files where n grams will be written
uniGramWriter.close()
biGramWriter.close()
triGramWriter.close()
quadGramWriter.close()

		



