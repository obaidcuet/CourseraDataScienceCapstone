import os, sys, re, csv

basePath = "C:/MyRoot/work/BigData/DataScience/Coursera Johns Hopkins Specialization in Data Science/Course Works/Capstone Project/textPredict"

# Assign sequentially incremental number to each of the words in the unigram file
# Later this assigned number will be used as index for the corresponding word
# Store the indexed words as a dictionary(key=word, value=index) in a jason file
def createWordIndex(infileName, outfileName):
	import csv, json
	
	input = open(infileName, "rt") # Open the unigram file
	reader = csv.reader(input)
	next(reader, None)  # skip the headers
	
	uniGrams = {}
	index = 0
	for row in reader:
		word = row[1]
		index = index + 1
		uniGrams[word]=index # assigne word as key and index as value
	input.close()
	
	# write the unigram or token index in a JASON file 
	with open(outfileName, 'w') as fp:
		json.dump(uniGrams, fp)
	

# read word index from the JASON file created using function "createWordIndex"
def readWordIndex(infileName):
	import csv, json
	with open(infileName, 'r') as fp:
		wordIndex = json.load(fp)
	return wordIndex # retrun as distionaly

# convert words in the unigram to number as per the out put of "createWordIndex"
# the input (unigram) file will be a csv file:
#	col0: frequency of the word,data type: number
#	col1: the unigram word, data type: string
# the output(indexed unigrams) of this function will be two column data frame:
# 	col0: frequency of the unigram, data type: number
#	col1: corresponding indexed number for the unigram word, data type: number
#	no header in the output file
# data <- read.csv("./finalNGrams/indexedUniGrams.csv", header=FALSE)
# names(data) <- c("freq", "wordIdx") 

def compressUnigrams(infileName, outfileName, wordIndex):
	import csv
	
	indexedUniGramWriter = open(outfileName, 'wt')
	
	input = open(infileName, "rt") # Open the unigram file
	reader = csv.reader(input)
	next(reader, None)  # skip the headers
	for row in reader:
		index = wordIndex.get(row[1])
		freq = row[0]
		indexedUniGramWriter.write(str(freq)+","+str(index)+"\n")
		
	input.close()
	indexedUniGramWriter.close()


# convert words in the bigram to number as per the out put of "createWordIndex"
# the input (bigram) file will be a csv file:
#	col0: frequency of the word,data type: number
#	col1: the biigram words, data type: string
# the output(indexed unigrams) of this function will be two column data frame:
# 	col0: frequency of the unigram, data type: number
#	col1: corresponding indexed number for the bigram 1st word, data type: number
#	col2: corresponding indexed number for the bigram 2nd word, data type: number
#	no header in the output file
# data <- read.csv("./finalNGrams/indexedBiGrams.csv", header=FALSE)
# names(data) <- c("freq", "wordIdx1", "wordIdx2") 
# data$freq <- as.integer(data$freq)
# data$wordIdx1 <- as.integer(data$wordIdx1)
# data$wordIdx2 <- as.integer(data$wordIdx2)

def compressBigrams(infileName, outfileName, wordIndex):
	import csv
	
	indexedBiGramWriter = open(outfileName, 'wt')
	
	input = open(infileName, "rt") # Open the bigram file
	reader = csv.reader(input)
	next(reader, None)  # skip the headers
	for row in reader:
		words = row[1].split()
		index1 = wordIndex.get(words[0])
		index2 = wordIndex.get(words[1])
		freq = row[0]
		indexedBiGramWriter.write(str(freq)+","+str(index1)+","+str(index2)+"\n")
		
	input.close()
	indexedBiGramWriter.close()
	

# convert words in the trigram to number as per the out put of "createWordIndex"
# the input (trigram) file will be a csv file:
#	col0: frequency of the word,data type: number
#	col1: the trigram words, data type: string
# the output(indexed unigrams) of this function will be two column data frame:
# 	col0: frequency of the unigram, data type: number
#	col1: corresponding indexed number for the trigram 1st word, data type: number
#	col2: corresponding indexed number for the trigram 2nd word, data type: number
#	col3: corresponding indexed number for the trigram 3rd word, data type: number
#	no header in the output file
# data <- read.csv("./finalNGrams/indexedTriGrams.csv", header=FALSE)
# names(data) <- c("freq", "wordIdx1", "wordIdx2", "wordIdx3") 
# data$freq <- as.integer(data$freq)
# data$wordIdx1 <- as.integer(data$wordIdx1)
# data$wordIdx2 <- as.integer(data$wordIdx2)
# data$wordIdx3 <- as.integer(data$wordIdx3)
def compressTrigrams(infileName, outfileName, wordIndex):
	import csv
	
	indexedTriGramWriter = open(outfileName, 'wt')
	
	input = open(infileName, "rt") # Open the trigram file
	reader = csv.reader(input)
	next(reader, None)  # skip the headers
	for row in reader:
		words = row[1].split()
		index1 = wordIndex.get(words[0])
		index2 = wordIndex.get(words[1])
		index3 = wordIndex.get(words[2])
		freq = row[0]
		indexedTriGramWriter.write(str(freq)+","+str(index1)+","+str(index2)+","+str(index3)+"\n")
		
	input.close()
	indexedTriGramWriter.close()
	
def compressQuadgrams(infileName, outfileName, wordIndex):
	import csv
	
	indexedQuadGramWriter = open(outfileName, 'wt')
	
	input = open(infileName, "rt") # Open the trigram file
	reader = csv.reader(input)
	next(reader, None)  # skip the headers
	for row in reader:
		words = row[1].split()
		index1 = wordIndex.get(words[0])
		index2 = wordIndex.get(words[1])
		index3 = wordIndex.get(words[2])
		index4 = wordIndex.get(words[3])
		freq = row[0]
		indexedQuadGramWriter.write(str(freq)+","+str(index1)+","+str(index2)+","+str(index3)+","+str(index4)+"\n")
		
	input.close()
	indexedQuadGramWriter.close()
	
	
	
# create and load word indexes
createWordIndex(basePath + "/finalNGrams/unigrams.csv", basePath + "/finalNGrams/unigramsidx.json")	
wordIndex = readWordIndex(basePath + "/finalNGrams/unigramsidx.json")

# compress Unigrams
compressUnigrams(basePath + "/finalNGrams/unigrams.csv", basePath + "/finalNGrams/indexedUniGrams.csv", wordIndex)	

# compress Bigrams
compressBigrams(basePath + "/finalNGrams/bigrams.csv", basePath + "/finalNGrams/indexedBiGrams.csv", wordIndex)	

# compress Trigrams
compressTrigrams(basePath + "/finalNGrams/trigrams.csv", basePath + "/finalNGrams/indexedTriGrams.csv", wordIndex)	

# compress Trigrams
compressQuadgrams(basePath + "/finalNGrams/quadgrams.csv", basePath + "/finalNGrams/indexedQuadGrams.csv", wordIndex)	
