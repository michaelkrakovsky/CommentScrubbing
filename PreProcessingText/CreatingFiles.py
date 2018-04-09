# Simple python text file that shows how to navigate through directories and create new files

import os
directory = os.fsencode(r"C:\Users\micha\Documents\Analytics & Coding\CryptoAnalysis\PythonSentimentAnalysis\PickleFiles\SubRedditPickledFiles")

for file in os.listdir(directory):
	fileName = os.fsdecode(file)
	newLocation = "C:\\Users\\micha\\Documents\\Analytics & Coding\\CryptoAnalysis\\PythonSentimentAnalysis\\PickleFiles\\SentimentValuesPickled\\"
	newLocation += fileName[:-25]
	newLocation += "SentimentDayScores.pickle"
	open(newLocation, "w+")