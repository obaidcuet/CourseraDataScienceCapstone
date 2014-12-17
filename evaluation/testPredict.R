library(stringr)
setwd("C:/MyRoot/work/BigData/DataScience/Coursera Johns Hopkins Specialization in Data Science/Course Works/Capstone Project/textPredict/finalNGrams")

wordDict <- readRDS("./unigramsidx.rds")        # numeric dictionary for words 
biGrams <- readRDS("./indexedBiGrams.rds")      # Loading BiGrams
triGrams <- readRDS("./indexedTriGrams.rds")    # Loading TriGrams
quadGrams <- readRDS("./indexedQuadGrams.rds") # Loading QuadGrams
pentaGrams <- readRDS("./indexedPentaGrams.rds") # Loading PentaGrams

## Default 3 predictions
defaultPredictStart = c("The", "To", "I") 
defaultPredictMiddle = c("the", "to", "I")

## get numeric value for a wors
getWordIdxValue <- function(word) {
        wordIdx <- as.numeric(wordDict[wordDict$words == word,2])
        if (length(wordIdx) > 0)
                wordIdx[1] # else retrun first value (avoid duplication)
        else 
                -1 # if not found retrun -1
}

## get the string value for a numeric value of a word
getWordStr <- function(wordidx) {
        word <- as.character(wordDict[wordDict$idx == wordidx,1])
        if (length(word) > 0)
                word[1] # else retrun first value (avoid duplication)
        else 
                "" # if not found retrun empty string ""
}

## series of cleaning before tokenization and prediction
numPuntuationCleaner <- function(inputStr) {
        # below steps should be done in sequence as here
        
        # 1.replace all back tick with single quote
        inputStr <- gsub("`", "'", inputStr, ignore.case = FALSE, perl = TRUE, fixed = FALSE, useBytes = FALSE)
        
        # 2.replace all except single quote, words[alpha numeric]
        inputStr <- gsub("[^\\w' ]", "", inputStr, ignore.case = FALSE, perl = TRUE, fixed = FALSE, useBytes = FALSE)
        
        # 3.replace all under score "_" with space
        inputStr <- gsub("[_]", " ", inputStr, ignore.case = FALSE, perl = TRUE, fixed = FALSE, useBytes = FALSE)
        
        # 4.replace all single quotes except apostrophe s,t,d & ve.
        # This should be done after replace all except single quote & words 	
        inputStr <- gsub("(?!'[stdm] |'ve |'re )'", " ", inputStr, ignore.case = FALSE, perl = TRUE, fixed = FALSE, useBytes = FALSE)
        
        # 5. Replace all standalone numbers and numbers that are start of word	
        inputStr <- gsub("^\\d+| \\d+|\\t+\\d+", " ", inputStr, ignore.case = FALSE, perl = TRUE, fixed = FALSE, useBytes = FALSE)
        
        # 6. Replace extra spaces and tabs with single spaces	
        inputStr <- gsub(" +|\t+", " ", inputStr, ignore.case = FALSE, perl = TRUE, fixed = FALSE, useBytes = FALSE)
        
        # 7. Repace starting and trailing spaces and tabs	
        inputStr <- gsub("^ +| +$|^\\t+|\\t+$", "", inputStr, ignore.case = FALSE, perl = TRUE, fixed = FALSE, useBytes = FALSE)
        
        #return
        inputStr
}

## check whether it is a start of a sentence
isStartSentence <- function(inputStr) {
        # replace trailing white spaces and tabs
        inputStr <- gsub(" +$|\\t+$", "", inputStr, ignore.case = FALSE, perl = TRUE, fixed = FALSE, useBytes = FALSE)
        # check for "." "?" "!" or ""[empty] coming at the end, if yes then retrun TRUE or FALSE
        grepl("\\.$|\\?$|\\!$|^$", inputStr, ignore.case = FALSE, perl = TRUE, fixed = FALSE, useBytes = FALSE)
}


# retrun last N number of nGrams(words). 
# nGrams should start from end of last sentence if there are multiple sentence
lastNGrams <- function(inputStr, N)	{
        if (isStartSentence(inputStr)) {
                "" # return empty string
        }
        else {
                splitVector <- strsplit(inputStr, "[.!?]", perl=TRUE) # take just last sentence
                lastSentence <- tail(unlist(splitVector),1)
                lastSentence <- numPuntuationCleaner(lastSentence)
                
                if (!isStartSentence(lastSentence))
                        tail(unlist(strsplit(lastSentence, " ")), N) # tokenize and return last N ngrams
                else
                        "" # if empty sentence after cleaning, retrun empty string
        }
}

# Prediction using bigrams
biGramPredict <- function(prevWord1) {
        word1Idx <- getWordIdxValue(prevWord1)
        satisfiedBigrams <- biGrams[biGrams$wordIdx1 == word1Idx, ]
        out <- sapply(head(satisfiedBigrams[order(satisfiedBigrams$freq, decreasing=T), "wordIdx2"], 3), getWordStr)
        if(length(out) == 3)
                out
        else if(length(out) == 2)
                c(out, defaultPredictMiddle[1])
        else if(length(out) == 1)
                c(out, defaultPredictMiddle[1], defaultPredictMiddle[2])
        else
                defaultPredictMiddle
}

# Prediction using trigrams
triGramPredict <- function(prevWord1, prevWord2) {
        word1Idx <- getWordIdxValue(prevWord1)
        word2Idx <- getWordIdxValue(prevWord2)
        
        satisfiedTrigrams <- triGrams[triGrams$wordIdx1 == word1Idx & triGrams$wordIdx2 == word2Idx , ]
        out <- sapply(head(satisfiedTrigrams[order(satisfiedTrigrams$freq, decreasing=T), "wordIdx3"], 3), getWordStr)
        if(length(out) == 3)
                out
        else if(length(out) == 2)
                c(out, defaultPredictMiddle[1])
        else if(length(out) == 1)
                c(out, defaultPredictMiddle[1], defaultPredictMiddle[2])
        else
                biGramPredict(prevWord2)
}

# Prediction using quadgrams
quadGramPredict <- function(prevWord1, prevWord2, prevWord3) {
        word1Idx <- getWordIdxValue(prevWord1)
        word2Idx <- getWordIdxValue(prevWord2)
        word3Idx <- getWordIdxValue(prevWord3)
        
        satisfiedQuadgrams <- quadGrams[quadGrams$wordIdx1 == word1Idx & quadGrams$wordIdx2 == word2Idx & quadGrams$wordIdx3 == word3Idx, ]
        out <- sapply(head(satisfiedQuadgrams[order(satisfiedQuadgrams$freq, decreasing=T), "wordIdx4"], 3), getWordStr)
        if(length(out) == 3)
                out
        else if(length(out) == 2)
                c(out, defaultPredictMiddle[1])
        else if(length(out) == 1)
                c(out, defaultPredictMiddle[1], defaultPredictMiddle[2])
        else
                triGramPredict(prevWord2,prevWord3)
}

# Prediction using pentagrams
pentaGramPredict <- function(prevWord1, prevWord2, prevWord3, prevWord4) {
        word1Idx <- getWordIdxValue(prevWord1)
        word2Idx <- getWordIdxValue(prevWord2)
        word3Idx <- getWordIdxValue(prevWord3)
        word4Idx <- getWordIdxValue(prevWord4)        
        
		satisfiedPentagrams <- pentaGrams[pentaGrams$wordIdx1 == word1Idx & pentaGrams$wordIdx2 == word2Idx & pentaGrams$wordIdx3 == word3Idx & pentaGrams$wordIdx4 == word4Idx, ]
        out <- sapply(head(satisfiedPentagrams[order(satisfiedPentagrams$freq, decreasing=T), "wordIdx5"], 3), getWordStr)
        if(length(out) == 3)
                out
        else if(length(out) == 2)
                c(out, defaultPredictMiddle[1])
        else if(length(out) == 1)
                c(out, defaultPredictMiddle[1], defaultPredictMiddle[2])
        else
                quadGramPredict(prevWord2,prevWord3,prevWord4)
}


# predict 3 probable next words, by upto 5-gram models
predictNextWord <- function (inputStr) {
        prevWords <- lastNGrams(inputStr, 4) # using last 4 words (N=4) to prodict next
        if (prevWords[1] == "")
                defaultPredictStart # start of line, so use the default prediction
        else { 
                if(length(prevWords)== 1)
                        biGramPredict(prevWords[1])
                else if (length(prevWords)== 2)
                        triGramPredict(prevWords[1], prevWords[2]) 
                else if (length(prevWords)== 3) 
                        quadGramPredict(prevWords[1], prevWords[2], prevWords[3])
                else if (length(prevWords)== 4) 
                        pentaGramPredict(prevWords[1], prevWords[2], prevWords[3], prevWords[4])
				else
                        defaultPredictMiddle
        }
}

replaceProfanity <- function(inprofanity, inStr) {
	gsub(paste( "\b",paste(profanity[,1] ,collapse="|"), "\b", sep="" ), " ", inStr, ignore.case = TRUE, perl = TRUE, fixed = FALSE, useBytes = FALSE)
}


######################################

# predict 3 probable next words, by upto 4-gram models
predictNextWord_model1 <- function (inputStr) {
        prevWords <- lastNGrams(inputStr, 3) # using last 3 words (N=3) to prodict next
        if (prevWords[1] == "")
                defaultPredictStart # start of line, so use the default prediction
        else { 
                if(length(prevWords)== 1)
                        biGramPredict(prevWords[1])
                else if (length(prevWords)== 2)
                        triGramPredict(prevWords[1], prevWords[2]) 
                else if (length(prevWords)== 3) 
                        quadGramPredict(prevWords[1], prevWords[2], prevWords[3])
                else
                        defaultPredictMiddle
        }
}

setwd("C:/MyRoot/work/BigData/DataScience/Coursera Johns Hopkins Specialization in Data Science/Course Works/Capstone Project/textPredict/test")

profanity <- read.csv("./profanity_words.txt", header=FALSE)
#data <- readRDS("./en_US.sampleTrain.rds") 
#data <- rbind(head(data[data$source=="news",],50), head(data[data$source=="blog",],50), head(data[data$source=="twitter",],50))
#saveRDS(data,"./testInsample.rds")

##data <- readRDS("./testInsample.rds") #150 lines from swiftkey
##data <- readRDS("./testOutsample.rds") #50 lines from ANC

total <- 0
success <- 0
saveKeyStroke <- 0
start <- Sys.time()
for ( i in seq(1:nrow(data)) ) {
	print(i)
	lines <- strsplit( as.character(data[i,2]), "\\.|\\?|!|,", perl = TRUE)
	lines <- sapply(lines, replaceProfanity, inprofanity = profanity)
	lines <- sapply(as.character(lines), numPuntuationCleaner)
	lines <- as.character(lines)
	
	for (sentence in lines) {
		#print(sentence)
		words <-  strsplit(sentence, " ")
		words <- words[[1]]
		currStr <- ""
		
		if(!is.na(words[1])) {
			total <- total+length(words)
			if(predictNextWord("")[1] == words[1])
				success <- success+1
			
			for ( i in seq(1:(length(words)-1)) ) {
				currStr <- paste(currStr, words[i], sep = " ")
				#print(str_trim(currStr))
				predicted <- predictNextWord(currStr)
				if( !is.na(predicted[1]) && !is.na(words[i+1]) && (predicted[1] == words[i+1])) {
					success <- success+1
					saveKeyStroke <- saveKeyStroke +(nchar(words[i+1]) - 1 )
					#print(paste("Success:", "Input:", currStr, "Predicted:", predicted[1], "Actual:", words[i+1], sep = " "))
				}
				#else
				#	print(paste("FAIL:", "Input:", currStr, "Predicted:", predicted[1], "Actual:", words[i+1], sep = " "))
			}
		}
	}
}
end <- Sys.time()
total
success
saveKeyStroke
end - start


(object.size(wordDict)+object.size(biGrams)+object.size(triGrams)+object.size(quadGrams))/1024/1024
(object.size(wordDict)+object.size(biGrams)+object.size(triGrams)+object.size(quadGrams)++object.size(pentaGrams))/1024/1024


