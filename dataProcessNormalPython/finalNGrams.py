import csv, os
from collections import defaultdict

basePath = "C:/MyRoot/work/BigData/DataScience/Coursera Johns Hopkins Specialization in Data Science/Course Works/Capstone Project/textPredict"

input = basePath+"/n-grams"

finalNgramPath = basePath+"/finalNGrams"

dirs = os.listdir(input)

for fileName in dirs:
	ngrams = defaultdict(int)
	with open(input+"/"+fileName) as infile:
		reader = csv.reader(infile)		
		for rows in reader:
			ngrams[rows[0]] += int(rows[1])

	with open(finalNgramPath+"/"+fileName, 'wt', newline='') as outfile:
		writer = csv.writer(outfile)
		for key, value in ngrams.items():
			writer.writerow([key, value])
			



