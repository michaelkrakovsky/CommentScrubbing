import pickle
import nltk
import time
import Vote_Classifiers
import os
import datetime 
# Posts are formatted in the following way: id, title, author, date, comment Number, crosspost Number, ups, Post Flag
# Comments are formatted in the following way: id, body, date, author, ups, Post Id

ORIGINALDIRECTORY = "C:\\Users\\micha\\Documents\\Analytics & Coding\\CryptoAnalysis\\PythonSentimentAnalysis\\PickleFiles\\SubRedditPickledFiles\\"
directory = os.fsencode(ORIGINALDIRECTORY)
now = datetime.datetime.now()

def status(currentLocation):
	timeElapsed = (datetime.datetime.now() - now).seconds / 60
	print(currentLocation + " Total elapsed time: " + str(timeElapsed))

for file in os.listdir(directory):
	
	fileName = os.fsdecode(file)
	fileName = ORIGINALDIRECTORY + fileName
	pickleFileToLoad = open(fileName, "rb")
	cryptoFile = pickle.load(pickleFileToLoad)
	pickleFileToLoad.close()
	
	# Step 1: Separate the datasets into comments and posts
	comments = []
	posts = []

	for i in cryptoFile:
		if (i[-1] == '1'):
			posts.append(i)
		else:
			comments.append(i)

	# Step 2: Create a dictionary and input the upvotes

	upVoteDictionary = {}
	for line in comments:
		date = int(line[2][:-2])
		upVotes = int(line[4])
		dateIndex = date - (date % 86400) 
		
		if dateIndex in upVoteDictionary:
			upVoteDictionary[dateIndex] += upVotes
		else:
			upVoteDictionary[dateIndex] = upVotes
			
	for line in posts:
		date = int(line[3][:-2])
		upVotes = int(line[6])
		dateIndex = date - (date % 86400) 
		
		if dateIndex in upVoteDictionary:
			upVoteDictionary[dateIndex] += upVotes
		else:
			upVoteDictionary[dateIndex] = upVotes
	
	status("Now moving to step 3.1 on file: " + fileName)
	# Step 3: Similar to step 2, except now we are performing a waited analysis 
	weightedVotedDictionary = {}
	for line in comments:
		date = int(line[2][:-2])
		upVotes = int(line[4])
		dateIndex = date - (date % 86400) 
		sentimentAnalysis = Vote_Classifiers.sentiment(line[1])    # Get sentiment value
		

		x = 0     # This value determines the weighting of the value
		if (sentimentAnalysis[0] == 'pos'):
			x = sentimentAnalysis[1]
		else:
			x = -1 * sentimentAnalysis[1]
		
		upVoteWeighter = upVotes / upVoteDictionary[dateIndex]
		dayValue = x * upVoteWeighter
		
		if dateIndex in weightedVotedDictionary:
			weightedVotedDictionary[dateIndex] += dayValue
		else:
			weightedVotedDictionary[dateIndex] = dayValue
	
	status("Now moving to step 3.2: " + fileName)
	
	for line in posts:
		date = int(line[3][:-2])
		upVotes = int(line[6])
		dateIndex = date - (date % 86400) 
		sentimentAnalysis = Vote_Classifiers.sentiment(line[1])    # Get sentiment value
		

		x = 0     # This value determines the weighting of the value
		if (sentimentAnalysis[0] == 'pos'):
			x = sentimentAnalysis[1]
		else:
			x = -1 * sentimentAnalysis[1]
		
		upVoteWeighter = upVotes / upVoteDictionary[dateIndex]
		dayValue = x * upVoteWeighter
		
		if dateIndex in weightedVotedDictionary:
			weightedVotedDictionary[dateIndex] += dayValue
		else:
			weightedVotedDictionary[dateIndex] = dayValue

	fileName = os.fsdecode(file)
	newLocation = "C:\\Users\\micha\\Documents\\Analytics & Coding\\CryptoAnalysis\\PythonSentimentAnalysis\\PickleFiles\\SentimentValuesPickled\\"
	newLocation += fileName[:-25]
	newLocation += "SentimentDayScores.pickle"
	fileToPickle = open(newLocation, "wb")
	pickle.dump(weightedVotedDictionary, fileToPickle)
	fileToPickle.close()
	
	print("The file has been pickled to " + newLocation)

print("The sentiment dictionaries has been created.")