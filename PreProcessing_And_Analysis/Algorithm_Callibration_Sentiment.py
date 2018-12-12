# Author: Michael Krakovsky
# Date: March 31, 2018
# Version 0.1
# Description: With the given feature sets we possess, create multiple algorithms that classify comments as either positive or negative.

import pickle
import nltk
import random
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.naive_bayes import MultinomialNB , BernoulliNB
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC

pickledFeatureSet = open(r"C:\Users\micha\Documents\Analytics & Coding\CryptoAnalysis\PythonSentimentAnalysis\PickleFiles\TrainingDataPickled\featureSetsPickled.pickle", "rb")
featureSets = pickle.load(pickledFeatureSet)     # Load the pickle set and put the data into a training set and a testing set		
random.shuffle(featureSets)           # Shuffle the feature sets to ensure randomization
trainingSetSize = int(len(featureSets) * 0.8)		# Create a training set that is 80% of the data
trainingSet = featureSets[:trainingSetSize]
testingSet = featureSets[trainingSetSize:]
pickledFeatureSet.close()

# Pickle the Testing set for use in other files
pickledTestingSet = open(r"C:\Users\micha\Documents\Analytics & Coding\CryptoAnalysis\PythonSentimentAnalysis\PickleFiles\TrainingDataPickled\testingSet.pickle", "wb")
pickle.dump(testingSet, pickledTestingSet)
pickledTestingSet.close()

# The following lines are just repeated. The file name and the model used are the only things that are replaced. Here is the format.
# variable_Name_of_Model = model_Name(trainingSet)
# variable_Name_of_File = open(file_Name, "wb")  
# pickle.dump(variable_Name_of_Model, variable_Name_of_File)
# variable_Name_of_File.close()  

classifierOriginalNB = nltk.NaiveBayesClassifier.train(trainingSet)
originalNBPickleFile = open(r"C:\Users\micha\Documents\Analytics & Coding\CryptoAnalysis\PythonSentimentAnalysis\PickleFiles\ClassifiersPickled\originalNB_Pickle_File.pickle", "wb")  
pickle.dump(classifierOriginalNB, originalNBPickleFile)
originalNBPickleFile.close()                 
print("Original Naive Bayes has been completed. The accuracy is: ", (nltk.classify.accuracy(classifierOriginalNB, testingSet)) * 100)

MNBClassifier = SklearnClassifier(MultinomialNB())
MNBClassifier.train(trainingSet)
MNBClassifierPickleFile = open(r"C:\Users\micha\Documents\Analytics & Coding\CryptoAnalysis\PythonSentimentAnalysis\PickleFiles\ClassifiersPickled\MNB_classifier.pickle", "wb")  
pickle.dump(MNBClassifier, MNBClassifierPickleFile)
MNBClassifierPickleFile.close() 
print("MNB Classifier has been completed. The accuracy is: ", (nltk.classify.accuracy(MNBClassifier, testingSet)) * 100)

BernoulliNBClassifier = SklearnClassifier(BernoulliNB())
BernoulliNBClassifier.train(trainingSet)
BernoulliNBFile = open(r"C:\Users\micha\Documents\Analytics & Coding\CryptoAnalysis\PythonSentimentAnalysis\PickleFiles\ClassifiersPickled\Bernoulli_NB.pickle", "wb")  
pickle.dump(BernoulliNBClassifier, BernoulliNBFile)
BernoulliNBFile.close() 
print("Bernoulli NB has been completed. The accuracy is: " , (nltk.classify.accuracy(BernoulliNBClassifier, testingSet)) * 100)

logisticRegressionClassifier = SklearnClassifier(LogisticRegression())
logisticRegressionClassifier.train(trainingSet)
logisticRegressionClassifierFile = open(r"C:\Users\micha\Documents\Analytics & Coding\CryptoAnalysis\PythonSentimentAnalysis\PickleFiles\ClassifiersPickled\logisticRegression_Classifier.pickle", "wb")  
pickle.dump(logisticRegressionClassifier, logisticRegressionClassifierFile)
logisticRegressionClassifierFile.close()
print("Logistic Regression Classifier has been completed. The accuracy is: ", (nltk.classify.accuracy(logisticRegressionClassifier, testingSet)) * 100)

SGDClassifierModel = SklearnClassifier(SGDClassifier())
SGDClassifierModel.train(trainingSet)
SGDClassifierModelFile = open(r"C:\Users\micha\Documents\Analytics & Coding\CryptoAnalysis\PythonSentimentAnalysis\PickleFiles\ClassifiersPickled\SGDClassifierModelFile.pickle", "wb")  
pickle.dump(SGDClassifierModel, SGDClassifierModelFile)
SGDClassifierModelFile.close()
print("SGD Classifier Model has been completed. The accuracy is: ", (nltk.classify.accuracy(SGDClassifierModel, testingSet)) * 100)

LinearSVCClassifeierModel = SklearnClassifier(LinearSVC())
LinearSVCClassifeierModel.train(trainingSet)
LinearSVCClassifeierFile = open(r"C:\Users\micha\Documents\Analytics & Coding\CryptoAnalysis\PythonSentimentAnalysis\PickleFiles\ClassifiersPickled\LinearSVCClassifeierFile.pickle", "wb")
pickle.dump(LinearSVCClassifeierModel, LinearSVCClassifeierFile)
LinearSVCClassifeierFile.close()
print("LinearSVC Model has been completed. The accuracy is: ", (nltk.classify.accuracy(LinearSVCClassifeierModel, testingSet)) * 100)

NuSVCClassifierModel = SklearnClassifier(NuSVC())
NuSVCClassifierModel.train(trainingSet)
NuSVCClassifierFile = open(r"C:\Users\micha\Documents\Analytics & Coding\CryptoAnalysis\PythonSentimentAnalysis\PickleFiles\ClassifiersPickled\NuSVCClassifierModel.pickle", "wb")
pickle.dump(NuSVCClassifierModel, NuSVCClassifierFile)
NuSVCClassifierFile.close()
print("NuSVC Model has been completed. The accuracy is: ", (nltk.classify.accuracy(NuSVCClassifierModel, testingSet)) * 100)

print("All models are loaded and primed.")  # Indicate the program as finished