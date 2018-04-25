# Read all the comments and posts from a subreddit
# Author: Michael Krakovsky
# Version 2.0
# Date: April 11, 2018
# In response to an outdated Reddit API, the old script became outdated. Therefore, we transfered from the praw
# API wrapper to the api.pushshift.io to scrub for comments.
# Posts are outlined: "postFlag", "id", "score", "created_utc", "title", "selftext", "author"
# Comments are outlined: "parent_id" (Serves as a post flag), "id", "score", "created_utc", "body", "link_id", "author"

import urllib.request, json             # Import the necessary files 
import pickle 
import time

END_DATE = 1523371381
INCREMENT_BY = 3600 * 48

# A list of tuples that indicate the subreddit names and time to start. This will be used to automate the process 
# All of the subreddits in the following list are all the subreddits we have analysed.
subredditsToParse = [("iungo", 1509547381), ("WePowerNetwork", 1514815654), ("fuzex", 1514815654), ("beetoken", 1514815654),  
					 ("republicprotocol", 1514815654), ("arcblock", 1514815654), ("Datawallet", 1514815654),
					 ("CurrentCRNC", 1514815654), ("Refereum", 1514815654), ("GBXCommunity", 1514815654), 
					 ("Dether", 1514815654), ("Globitex", 1514815654), ("FusionFSN", 1514815654), 
					 ("fundrequest", 1509545254), ("windingtree", 1514815654), ("syncfab", 1512137254), 
					 ("remme", 1514815654), ("CreditsOfficial", 1515593254), ("dockio", 1514815654), 
					 ("getBABB", 1514815654), ("TE_FOOD", 1515593254), ("Electrify", 1515593254), 
					 ("DebitumNetwork", 1514815654), ("huobi", 1514815654), ("havven", 1515593254), 
					 ("LYMPO", 1515593254), ("NapoleonX", 1514815654), ("HeroToken", 1514815654), 
					 ("AdHive", 1515593254), ("FintruX", 1514815654), ("Bankera", 1509545254), 
					 ("Rentberry", 1509545254), ("accord", 1514815654), ("Graft", 1514815654), 
					 ("0xProject", 1498918054), ("AionNetwork", 1509545254), ("Electroneum", 1498918054), 
					 ("nebulas", 1509545254), ("NucleusVision", 1512137254), ("SaltCoin", 1498918054), 
					 ("selfkey", 1509545254), ("THEKEYOFFICIAL", 1506866854), ("Tomochain", 1517494054), 
					 ("ZEEPIN", 1512137254), ("zilliqa", 1512137254)
					]
# These are only the subreddits that currently need processing because of a failed first attempt
selectedFew = [("Banca", 1515273326), ("CLN", 1516914926), 
				("Copytrack", 1511126126), ("Coin_Lion", 1511903726), ("EBCoin", 1511817326), 
				("EximChain", 1511730926), ("InsightsNetwork", 1510348526), ("LenDroid", 1517260526), 
				("PayPro", 1514322926), ("Quantocoin", 1511212526)
				]

# Function Description: Write selected information to a text file to ensure data is accurate
# Parameters: startTime (When the program started), numberComments (The number of comments gathered), numberSubmissions (Number of submissions gathered), 
# subreddit (The name of the subreddit), begDate (Starting date of the scrubbing processes), elementsSkipped (Instances that could not be processed)
# Throws: None
# Returns: None

def writeReportToFile(startTime, numberComments, numberSubmissions, subreddit, begDate, elementsSkipped):
	
	currentTime = time.time()			
	with open(r"C:\Users\micha\Dropbox\RedditComment\PushShift_Files_Reports\PickleReports.txt", "a") as file:
		file.write("\nSubreddit Scrubbed: " + subreddit + '\n')
		file.write("Total time to complete: " + str((currentTime - startTime) / 60) + ' min \n')
		file.write("Number of Comments: " + str(numberComments) + '\n')
		file.write("Number of Posts: " + str(numberSubmissions) + '\n')
		file.write("The number of elements skipped: " + str(numberOfSkipped) + '\n')
		file.write("The scrubbing began on: " + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(begDate)) + '\n')

# Function Description: Print informative statements to the screen indicating what is going on
# Parameters: startTime (When the program started), numberComments (The number of comments gathered), numberSubmissions (Number of submissions gathered)
# dayBeingProcessed (The day that is currently being processed by the loop)
# Throws: None
# Returns: None

def activateBeacon(numberComments, numberSubmissions, startTime, dayBeingProcessed):	
	currentTime = time.time()
	timeElaspsed = (currentTime - startTime) / 60
	print("Currently processing day: ", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(dayBeingProcessed)), "-- Time Elapsed (min): ", timeElaspsed)
	print("The number of comments and submissions gathered in total: ", numberComments, " & ", numberSubmissions)
	
# Function Description: Create a pickle file and insert Reddit content
# Parameters: subreddit (Name of the subreddit), listToPickle (The contents that need to be pickled)
# Throws: None
# Returns: None

def createPickleFiles(subreddit, listToPickle):
	
	fileName = r"C:\Users\micha\Dropbox\RedditComment\PushShift_Created_Pickle_Files"
	fileName += "\\" + subreddit + "_data.pickle" 
	file = open(fileName, "w+")
	file.close()
	
	with open(fileName, "wb") as file:
		pickle.dump(listToPickle, file, protocol=pickle.HIGHEST_PROTOCOL)
	
# Function Description: The function will create a string to acquire JSON data
# Parameters: date (The date to acquire the data), subreddit (The subreddit that is being analyzed) type (Whether you are searching for submission or comment)
# Throws: None
# Returns: urlString (A string that can be executed for url code)
# Example: URL outputs:
# https://api.pushshift.io/reddit/search/submission/?subreddit=NEO&after=1523269172&before=1523272772&size=500
# https://api.pushshift.io/reddit/search/comment/?subreddit=NEO&after=1523269172&before=1523272772&size=500
# The ending of the final string indicates the search query

def createURLString(date, subreddit, type):

	urlString = "https://api.pushshift.io/reddit/search/"       # Start out with the base, this will not change
	
	urlString += type + '/?'   								# Add whether it is a comment or string
	urlString += "subreddit=" + subreddit + "&"				# Add the subreddit you wish to search
	urlString += "after=" + str(date) + "&before=" + str(date + (INCREMENT_BY - 1)) + "&"         # The 3600 indicates a move forward by an hour at a time
	urlString += "size=500"     			# This indicates the number of items on the page (This is the maximum)
	return urlString

# Function Description: The function will open a url and put its contents within a dictionary
# Parameters: urlString (A string that can be executed for url code)
# Throws: None
# Returns: data (The data with the JSON content)

def gatherJSONData(urlString):

	with urllib.request.urlopen(urlString) as url:		# Open URL and store JSON data
		data = json.loads(url.read().decode())                  
	return data

# Function Description: Gather the necessary data points in a 'submission' query	
# Parameters: data (A JSON file), listToAppend (A list where nodes will be continually appended to)
# Throws: None
# Returns: None
# Posts are outlined: "postFlag", "id", "score", "created_utc", "title", "selftext", "author"

def retrieveSubmissionData(data, listToAppend):
	
	for instance in data["data"]:                # There is only one key in the dictionary and its called "data"    
		try:
			keyData = {}
			keyData["post_Flag"] = 1
			keyData["author"] = instance["author"]			# Add all the submission data
			keyData["created_utc"] = instance["created_utc"]
			try:
				keyData["selftext"] = instance["selftext"]
			except:
				keyData["selftext"] = None
				print("A selftext value was skipped")
			keyData["title"] = instance["title"]
			keyData["id"] = instance["id"]
			keyData["score"] = instance["score"]
			listToAppend.append(keyData)
		except:
			global numberOfSkipped		# For the record, I dislike global variables; however, it comes handy in this situation
			numberOfSkipped += 1
			print("An error has occurred here: ", instance)

# Function Description: Gather the necessary data points in a 'comment' query	
# Parameters: data (A JSON file), listToAppend (A list where nodes will be continually appended to)
# Throws: None
# Returns: None
# Comments are outlined: "parent_id" (Serves as a post flag), "id", "score", "created_utc", "body", "link_id", "author"

def retrieveCommentData(data, listToAppend):
	
	for instance in data["data"]:                # There is only one key in the dictionary and its called "data"  
		try:
			keyData = {}
			keyData["parent_id"] = instance["parent_id"]
			keyData["author"] = instance["author"]			# Add all the submission data
			keyData["created_utc"] = instance["created_utc"]
			keyData["body"] = instance["body"]
			keyData["score"] = instance["score"]
			keyData["link_id"] = instance["link_id"]
			listToAppend.append(keyData)
		except:
			global numberOfSkipped		# Again for the record, I dislike global variables; however, it comes handy in this situation
			numberOfSkipped += 1
			print("An error has occurred here: ", instance)


for tokenTuple in selectedFew:
	subredditName = tokenTuple[0] 		# Begin to scrape through all the indicate Subreddits (name, start time)
	startDate = tokenTuple[1]
	startTime = time.time()		# Track how long the subreddit takes to scrub
	counter = 0					# Used to activate beacon
	countSubmissions = 0		# Track number of posts
	numberOfSkipped = 0			# Keep track of number of bodies skipped
	countComments = 0			# Keep track of number of comments pulled
	postData = []		# This will store all the indicated data (Reset the list after every iterate through)
	commentData = []
	allData = (postData, commentData)      # This will be stored in a pickle file later
	print("\nBeginning to scrape Reddit comments on " + subredditName + ".")

	# Loop from a start date to an end date scraping all Reddit data. Increment by one hour to ensure all data is captured.
	for i in range(startDate, END_DATE, INCREMENT_BY):

		urlString = createURLString(i, subredditName, "submission")      # Add all posts in date range
		data = gatherJSONData(urlString)
		countSubmissions += len(data['data'])
		retrieveSubmissionData(data, postData)
		
		urlString = createURLString(i, subredditName, "comment")      # Add all comments in date range
		data = gatherJSONData(urlString)
		countComments += len(data['data'])
		retrieveCommentData(data, commentData)
		
		counter += 1
		if (counter >= 250):			# Raise the beacon after 250 iterations
			activateBeacon(countComments, countSubmissions, startTime, i)
			counter = 0
	
	writeReportToFile(startTime, countComments, countSubmissions, subredditName, startDate, numberOfSkipped)     # Write the final report
	createPickleFiles(subredditName, allData)     			# Pickle the files 
	print("\nThe subreddit " + subredditName + " has been scraped and recorded.")
	
print("The program is finished, the files are pickled!")					# Indicate the finish
