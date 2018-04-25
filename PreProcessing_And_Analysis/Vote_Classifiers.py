# Author: Michael Krakovsky
# Date: March 31, 2018
# Version 0.1
# Description: The program perform the classifying analytics by taking a pre-determined set, creating a classifier model and then determining 
# whether the comment is a negative one or a positive. There will also be a 'VoteClassifier' feature, where all of the models will have the ability
# to vote whether the comment is negative or positive.

import nltk
import random
from nltk.classify.scikitlearn import SklearnClassifier
import pickle
from sklearn.naive_bayes import MultinomialNB, GaussianNB, BernoulliNB
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC
from nltk.classify import ClassifierI
from statistics import mode
from nltk.tokenize import word_tokenize

# Description: The class will take a list of classifier models and will allow all of the models to vote whether the comment is negative or positive.
# Parameters: *classifiers (A list of classifiers that have been trained on the training set)
# Throws: None
# Return: N/A

class VoteClassifier(ClassifierI):

	# Description: The init will take the parameters and put them in a list called self._classifiers
	# Parameters: *classifiers (A tuple of classifiers that have been trained on the training set)
	# Throws: None
	# Return: None
	
	def __init__(self, *classifiers):
		self._classifiers = classifiers
	
	# Description: Each classifier will then have a chance to vote on what they believe to be negative or positive
	# Parameters: features (The method will accept a Dictionary of words indicating which key words were in the comment)
	# Throws: None
	# Return: mode(votes) (The highest frequency of whether pos or neg was voted) 
	
	def classify(self, features):
		votes = []
		for model in self._classifiers:			# Iterate through the classifier
			modelVote = model.classify(features)   # Allow the classifier to vote
			votes.append(modelVote)			
		return mode(votes)
	
	# Description: The method will return how confident it believes the guess to be 
	# Parameters: features (The method will accept a Dictionary of words indicating which key words were in the comment)
	# Throws: None
	# Return: conf (The confidence level of what it believes that guess to be)
	
	def confidence(self, features):
		votes = []
		for model in self._classifiers:
			modelVote = model.classify(features)
			votes.append(modelVote)
		choiceVotes = votes.count(mode(votes))
		confidenceLevel = choiceVotes / len(votes)
		return confidenceLevel
		
		
# The models will be loaded from their respected pickle files. Once loaded, they will be run through the Vote_classifier
pickleAlgorithmSet = open(r"C:\Users\micha\Documents\Analytics & Coding\CryptoAnalysis\PythonSentimentAnalysis\PickleFiles\ClassifiersPickled\Bernoulli_NB.pickle", "rb")
bernoulliNBModel = pickle.load(pickleAlgorithmSet)
pickleAlgorithmSet.close()

pickleAlgorithmSet = open(r"C:\Users\micha\Documents\Analytics & Coding\CryptoAnalysis\PythonSentimentAnalysis\PickleFiles\ClassifiersPickled\LinearSVCClassifeierFile.pickle", "rb")
LinearSVCClassifeierModel = pickle.load(pickleAlgorithmSet)
pickleAlgorithmSet.close()

pickleAlgorithmSet = open(r"C:\Users\micha\Documents\Analytics & Coding\CryptoAnalysis\PythonSentimentAnalysis\PickleFiles\ClassifiersPickled\logisticRegression_Classifier.pickle", "rb")
logisticRegressionClassifierModel = pickle.load(pickleAlgorithmSet)
pickleAlgorithmSet.close()

pickleAlgorithmSet = open(r"C:\Users\micha\Documents\Analytics & Coding\CryptoAnalysis\PythonSentimentAnalysis\PickleFiles\ClassifiersPickled\MNB_classifier.pickle", "rb")
MNBClassifierModel = pickle.load(pickleAlgorithmSet)
pickleAlgorithmSet.close()

pickleAlgorithmSet = open(r"C:\Users\micha\Documents\Analytics & Coding\CryptoAnalysis\PythonSentimentAnalysis\PickleFiles\ClassifiersPickled\NuSVCClassifierModel.pickle", "rb")
NuSVCClassifierModel = pickle.load(pickleAlgorithmSet)
pickleAlgorithmSet.close()

pickleAlgorithmSet = open(r"C:\Users\micha\Documents\Analytics & Coding\CryptoAnalysis\PythonSentimentAnalysis\PickleFiles\ClassifiersPickled\originalNB_Pickle_File.pickle", "rb")
originalNBModel = pickle.load(pickleAlgorithmSet)
pickleAlgorithmSet.close()

pickleAlgorithmSet = open(r"C:\Users\micha\Documents\Analytics & Coding\CryptoAnalysis\PythonSentimentAnalysis\PickleFiles\ClassifiersPickled\SGDClassifierModelFile.pickle", "rb")
SGDClassifierModelFile = pickle.load(pickleAlgorithmSet)
pickleAlgorithmSet.close()

#pickledTestingSet = open(r"C:\Users\micha\Documents\Analytics & Coding\CryptoAnalysis\PythonSentimentAnalysis\PickleFiles\TrainingDataPickled\testingSet.pickle", "rb")
#testingSet = pickle.load(pickledTestingSet)
#pickledTestingSet.close()

pickledFeatures = open(r"C:\Users\micha\Documents\Analytics & Coding\CryptoAnalysis\PythonSentimentAnalysis\PickleFiles\TrainingDataPickled\featureSetsPickled.pickle", "rb") 
featureSets = pickle.load(pickledFeatures)
pickledFeatures.close()

pickledFeatures = open(r"C:\Users\micha\Documents\Analytics & Coding\CryptoAnalysis\PythonSentimentAnalysis\PickleFiles\TrainingDataPickled\wordFeaturesPickled.pickle", "rb") 
wordFeatures = pickle.load(pickledFeatures)
pickledFeatures.close()

pickledFeatures = open(r"C:\Users\micha\Documents\Analytics & Coding\CryptoAnalysis\PythonSentimentAnalysis\PickleFiles\TrainingDataPickled\testingSet.pickle", "rb") 
testingSet = pickle.load(pickledFeatures)
pickledFeatures.close()

# Description: Determines whether the word from a comment exists within a tuple of words that typically exist in negative comments
# Parameters: document (A lsit that stores all the comments in a tuple indicating whether it is a positive or negative comment)
# Throws: None
# Return: features (A dictionary that indicates the word, and if it is in the top words mentioned)

def findFeatures(document):
	words = word_tokenize(document)     # Convert to set so data only appears once
	features = {}
	for w in wordFeatures:      # Iterate through the top 3000 words
		features[w] = (w in words)    # Indicate if the word is within the array
	return features

voted_classifier = VoteClassifier(bernoulliNBModel, 
								  LinearSVCClassifeierModel, 
								  logisticRegressionClassifierModel, 
								  MNBClassifierModel, 
								  NuSVCClassifierModel, 
								  originalNBModel, 
								  SGDClassifierModelFile) 

def sentiment(text):    # Return what the classifier returns and the probability of it being that respected class.
	feats = findFeatures(text)
	return voted_classifier.classify(feats), voted_classifier.confidence(feats) 

print("Comments are ready to be scrubbed!")