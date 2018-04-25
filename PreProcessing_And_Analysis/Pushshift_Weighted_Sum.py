# File Description: The file will classify whether comments are positive or negative and created a weighted sentiment score.
# Author: Michael Krakovsky
# Version 2.0
# Date: April 12, 2018
# Posts are outlined: "postFlag", "id", "score", "created_utc", "title", "selftext", "author"
# Comments are outlined: "parent_id" (Serves as a post flag), "id", "score", "created_utc", "body", "link_id", "author"

import pickle				# Import the necessary packages
import nltk
import time
import Vote_Classifiers
import os
import datetime 

print("Vote_Classifiers as been primed. Ready to run analysis.")

DIRECTORY_TO_ANALYSE = r"C:\Users\micha\Dropbox\RedditComment\PushShift_Created_Pickle_Files"
directory = os.fsencode(DIRECTORY_TO_ANALYSE)
contentSkipped = 0
progressCounter = 0

# Function Description: Ensure the string is important to be included in the analysis
# Parameters: stringToAnalyse (The string to be analyzed)
# Throws: None
# Returns: isGood (Boolean: True when the string is legit and False otherwise)

def performChecks(stringToAnalyse):
	
	if (stringToAnalyse == '[deleted]'):			# Enter the requirements in one big if statement. The following could be adjusted if need be.
		return False
	else:
		return True

# Function Purpose: Activate a beacon that indicates the progress of the data scrubbing
# Parameters: startTime (When the file started to be analyzed)
# Throws: None
# Returns: None

def activateBeacon(startTime):
	
	currentTime = time.time()
	global progressCounter
	
	print("The file is still being processed. Accumulative time to process file: " + str((currentTime - startTime) / 60) + " min")		# Indicate the time elapsed for the file
	progressCounter = 0							# Reset the progress counter		

# Function Purpose: Remove bad data from the post data set
# Parameters: dataSetToAnalyse (List of posts (which are dictionaries) that require cleaning)
# Throws: None
# Returns: None

def cleanPostDictionary(dataSetToAnalyse):	
	
	global contentSkipped 							# Record the amount of content that was skipped
	
	for idx, instance in enumerate(dataSetToAnalyse):			# Delete the element from the list if the element does not fit standards
		goodTitle = performChecks(instance['title'])
		if (goodTitle == False):
			dataSetToAnalyse.pop(idx)					
			contentSkipped += 1

# Function Purpose: Remove bad data from the comment data set
# Parameters: dataSetToAnalyse (List of comments (which are dictionaries) that require cleaning)
# Throws: None
# Returns: None

def cleanCommentDictionary(dataSetToAnalyse):	
	
	global contentSkipped 							# Record the amount of content that was skipped
	
	for idx, instance in enumerate(dataSetToAnalyse):			# Delete the element from the list if the element does not fit standards
		goodTitle = performChecks(instance['body'])
		if (goodTitle == False):
			dataSetToAnalyse.pop(idx)					
			contentSkipped += 1			
			
# Function Description: Create a pickle file and dictionary with dates
# Parameters: originalFileName (Name of the original pickled file with the scrubbed data), dictToPickle (The contents that need to be pickled)
# Throws: None
# Returns: None

def createPickleFiles(originalFileName, dictToPickle):
	
	fileName = r"C:\Users\micha\Dropbox\RedditComment\PushShift_Weighted_Scores"
	fileName += "\\sentimentScore_" + originalFileName 
	file = open(fileName, "w+")
	file.close()
	
	with open(fileName, "wb") as file:
		pickle.dump(dictToPickle, file, protocol=pickle.HIGHEST_PROTOCOL)

# Function Description: Load a previously created pickle file
# Parameters: fileName (The name of the file), initialDir (The name of the directory where the file is located)
# Throws: None
# Return: content (The content within the pickle file)
	
def loadAPickleFile(fileName, initialDir):

	file = open(initialDir + "\\" + fileName, "rb")		# Complete pickling procedure
	content = pickle.load(file)
	file.close()
	return content

# Function Description: Receive Reddit content and get the counts per day
# Parameters: redditContentTuple (The content from the pickle file)
# Throws: None
# Returns: scoreCountDictionary (Dictionary with the sum of scores for each day)
	
def countVotesInTheDay(redditContentTuple):
	
	scoreCountDictionary = {}		# Holds the count for the day
	
	for type in redditContentTuple:          # Loop through submissions and	comments
		for instance in type:				# Loop through the entire dictionary
			try: 
				date = instance['created_utc']				# The date from the reddit content
				dateIndex = date - (date % 86400)			# Bring the date to the beginning of the day
				if dateIndex in scoreCountDictionary:						# Add the score into the dictionary or create a new index
					scoreCountDictionary[dateIndex] += instance['score']
				else:
					scoreCountDictionary[dateIndex] = instance['score']
			except:
				print(10 * "#" + "There was an error indexing the date. Element skipped." + 10 * "#")
	return scoreCountDictionary

# Function Description: Calculate the sentiment score and update the appropriate dictionary
# Parameters: weightedScoreDictionary (Dictionary containing the weighted scores) dayCounter (Dictionary of either the number of posts or comments in the day)
# scoreCountDictionary (Dictionary containing the sum of scores in each day) dateCreated (Integer indicating when the content was created), 
# content (String containing the Reddit comment or post) score (The score the Reddit content received)
# Throws: None
# Returns: None
			
def performSentimentCalculation(weightedScoreDictionary, dayCounter, scoreCountDictionary, dateCreated, content, score):
	
	try:
		dateIndex = dateCreated - (dateCreated % 86400)					# Bring the date that the Reddit comment was created to the beginning of the day
		sentimentScoreTitle = Vote_Classifiers.sentiment(content)		# Get sentiment score in tuple form
		sentimentScore = 0
		
		if (sentimentScoreTitle[0] == 'pos'):			# Determine whether the sentiment score will be positive or negative
			sentimentScore = sentimentScoreTitle[1]
		else:
			sentimentScore = -1 * sentimentScoreTitle[1]
			
		upVoteWeighter = sentimentScore * (score / scoreCountDictionary[dateIndex])     # Add the weighted score to the dictionary
		
		if dateIndex in weightedScoreDictionary:
			weightedScoreDictionary[dateIndex] += upVoteWeighter
		else:
			weightedScoreDictionary[dateIndex] = upVoteWeighter
			
		if dateIndex in dayCounter:														# Keep track of the amount of posts for each day
			dayCounter[dateIndex] += 1
		else:
			dayCounter[dateIndex] = 1	
	except:
		print(10 * "#" + "We cannot get sentiment from this post title." + 10 * "#")	
	
# Function Description: The function creates a dictionary with weighted terms
# Parameters: posts (Only posts containing with the content) weightedScoreDictionary (Dictionary containing the weighted scores)
# scoreCountDictionary (Dictionary containing the sum of scores in each day) postsEachDay (Count the number of posts each day), startTime (When the for loop started)
# Throws: None
# Return: None
	
def weightedScoreCalculatorForPosts(posts, weightedScoreDictionary, postsEachDay, scoreCountDictionary, startTime):
	
	global progressCounter
	
	for instance in posts:			# Loop through only the posts
		try:
			performSentimentCalculation(weightedScoreDictionary, postsEachDay, scoreCountDictionary, instance['created_utc'], instance["title"], instance['score'])
		except:
			print(10 * "#" + "We cannot get sentiment from this post title." + 10 * "#")
			
		progressCounter += 1
		if (progressCounter >= 500):
			activateBeacon(startTime)
			
# Function Description: The function changes a dictionary with weighted terms
# Parameters: comments (Only comments containing with the content) weightedScoreDictionary (Dictionary containing the weighted scores)
# scoreCountDictionary (Dictionary containing the sum of scores in each day), commentsEachDay (Dictionary that tracks the comments each day), 
# startTime (Indicates when the file began to be processed)
# Throws: None
# Return: None

def weightedScoreCalculatorForComments(comments, weightedScoreDictionary, commentsEachDay, scoreCountDictionary, startTime):
	
	global progressCounter
	
	for instance in comments:			# Loop through only the comments
		try:				
			performSentimentCalculation(weightedScoreDictionary, commentsEachDay, scoreCountDictionary, instance['created_utc'], instance["body"], instance['score'])				
		except:
			print(10 * "#" + "We cannot get sentiment from this comment body." + 10 * "#")
			
		progressCounter += 1					# Indicate that a comment has been analyzed
		if (progressCounter >= 500):
			activateBeacon(startTime)
			
			
for file in os.listdir(directory):					# Loop through all the files in the entire directory
	
	fileName = os.fsdecode(file)		# Stores only the file name
	content = loadAPickleFile(fileName, DIRECTORY_TO_ANALYSE)    # Load the pickle file into the dictionary
	print("The file:", fileName, " as been loaded. Beginning to run sentiment analysis.")
	startTime = time.time()
	
	cleanPostDictionary(content[0])			# Clean the dictionaries to be processed (Passed by reference)
	cleanCommentDictionary(content[1])
	
	scoreCountDictionary = countVotesInTheDay(content)     # Create dictionary with the sum of scores for each day
	weightedScoreDictionary = {}			# Dictionary with all the weighted scores
	commentsEachDay = {}					# Track comments and posts each day
	postsEachDay = {}
	
	weightedScoreCalculatorForPosts(content[0], weightedScoreDictionary, commentsEachDay, scoreCountDictionary, startTime)		# Insert the weighted scores of the posts
	weightedScoreCalculatorForComments(content[1], weightedScoreDictionary, postsEachDay, scoreCountDictionary, startTime)		# Insert the weighted scores of the comments
	
	individualDicts = (weightedScoreDictionary, commentsEachDay, postsEachDay, scoreCountDictionary)
	createPickleFiles(fileName, individualDicts)		# Pickle the tuple of data into a dictionary and store
	print("The file:", fileName, " as been pickled. \n")

print("The dictionaries have been created.")


















