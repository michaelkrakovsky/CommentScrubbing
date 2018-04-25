# Author: Michael Krakovsky
# Date: March 31, 2018
# Version 0.1
# Description: Create multiple pickle files that store the preprocessed data. A pickle file will be created for:
#	featureSets
# The pickled dictionary contains a list of dictionaries. The dictionaries contain the word, whether they appear, and what type of comments they appear in.

from nltk.tokenize import word_tokenize
import nltk
import pickle

POSITIVE_COMMENTS_FILE = r"C:\Users\micha\Desktop\PositiveRedditComments.txt"     # Constants for the training set files
NEGATIVE_COMMENTS_FILE = r"C:\Users\micha\Desktop\NegativeRedditCommetns.txt"

shortPositiveComments = open(POSITIVE_COMMENTS_FILE, "r").read()
shortNegativeComments = open(NEGATIVE_COMMENTS_FILE, "r").read()
	
documents = []    # A list that stores all the comments in a tuple indicating whether it is a positive or negative comment	
allWords = []      # Separate all the words associated with positive / negative into distinct tuples

# J is considered adjective. R is adverb, and V is considered a verb
allowedWordTypes = ["J", "V", "P"]

for comment in shortPositiveComments.split('\n'):     
	documents.append( (comment, 'pos') )
	words = word_tokenize(comment)
	pos = nltk.pos_tag(words)
	for w in pos:
		if w[1][0] in allowedWordTypes:
			allWords.append(w[0].lower())
	
for comment in shortNegativeComments.split('\n'):
	documents.append( (comment, 'neg') )
	words = word_tokenize(comment)
	pos = nltk.pos_tag(words)
	for w in pos:
		if w[1][0] in allowedWordTypes:
			allWords.append(w[0].lower())
	
documentsPickled = open(r"C:\Users\micha\Documents\Analytics & Coding\CryptoAnalysis\PythonSentimentAnalysis\PickleFiles\TrainingDataPickled\documents.pickle", "wb")  # Write the feature set to a pickle file
pickle.dump(documents, documentsPickled)
documentsPickled.close()

allWords = nltk.FreqDist(allWords)
wordFeatures = list(allWords.keys())[:5000]     # Limit the amount of words we train against

wordFeaturesPickled = open(r"C:\Users\micha\Documents\Analytics & Coding\CryptoAnalysis\PythonSentimentAnalysis\PickleFiles\TrainingDataPickled\wordFeaturesPickled.pickle", "wb")  # Write the feature set to a pickle file
pickle.dump(wordFeatures, wordFeaturesPickled)
wordFeaturesPickled.close()

# Description: Determines whether the word from a comment exists within a tuple of words that typically exist in negative comments
# Parameters: document (A lsit that stores all the comments in a tuple indicating whether it is a positive or negative comment)
# Throws: None
# Return: features (A dictionary that indicates the word, and if it is in the top words mentioned)

def findFeatures(document):
	words = word_tokenize(document)     # Convert to set so data only appears once
	features = {}
	for w in wordFeatures:      # Iterate through the top words
		features[w] = (w in words)    # Indicate if the word is within the array
	return features
	
featureSets = [(findFeatures(rev), category) for (rev, category) in documents]

featuresSetsPickled = open(r"C:\Users\micha\Documents\Analytics & Coding\CryptoAnalysis\PythonSentimentAnalysis\PickleFiles\TrainingDataPickled\featureSetsPickled.pickle", "wb")  # Write the feature set to a pickle file
pickle.dump(featureSets, featuresSetsPickled)
featuresSetsPickled.close()

print("The sample set as been pickled.") # Indicate the end of the script