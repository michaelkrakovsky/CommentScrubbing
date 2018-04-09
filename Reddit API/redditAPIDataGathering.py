# Read all the comments from a subreddit
# Author: Michael Krakovsky
# Version 1.1
# Date: March 7, 2018

import sys
from RetrievingRedditPosts import redditPosts 
from ParsingTechniques import parsingQueries
import praw
import calendar
import time

START_DATE = 1501608603    # Create a beginning date and an end date 
END_DATE = 1521427200
INTERVAL_TIME = 86400
LIMIT_NUM = 200         # Indicates the number of reddit comments per request
DELAY_TIME = 2     # Seconds is the amount of time the program will be temporarily halted
FILENAME = 'C:\\Users\\micha\\Desktop\\zilliqa.txt'
SUBREDDIT_NAME = 'zilliqa'

reddit = praw.Reddit(client_id= 'ouSaZ-95Dd2cTA',       # Create a reddit instance
						client_secret= 'D2D4SpowSg925-qWfxIJA_NWX0k',
						username= 'mkracker', 
						password= 'thisismyredditaccount', 
						user_agent= 'CryptoCurrenciesChats.myredditapp:v1.0 (by /u/mkracker')

# Meta data variables that store results about the run
commentsSkipped = 0
numCommentsProcessed = 0
numPostsProcessed = 0
begRunTime = calendar.timegm(time.gmtime()) 

# Function Purpose: Print the run stats of the Reddit 
# Parameters: begRunTime (When the program started)
# Throws: None
# Return: None
def printReport(begRunTime): 
	
	totalRunTime = 0
	endRunTime = calendar.timegm(time.gmtime()) 
	totalRunTime = (endRunTime - begRunTime) / 60
	print("Finished retrieving data from subreddit: ", SUBREDDIT_NAME)
	print("The number of posts processed: ", numPostsProcessed)
	print("The number of comments processed: ", numCommentsProcessed)
	print("The number of comments skipped: ", commentsSkipped)
	print("The total run time is (in minutes): ", totalRunTime)
						
# Function Purpose: Write a designated string to a particular file
# Parameters: stringToWrite (The string that will be written), entering (Assumes the program is entering a comment tree)
# Throws: None
# Return: None
						
def writeToFile(stringToWrite, entering=2):

	with open(FILENAME, "a", encoding='utf8') as outfile:
		outfile.write(stringToWrite)
		if (entering == 1):
			outfile.write("-----Entering the comment tree.-----\n")
		elif (entering == 0):
			outfile.write("-----Exiting the comment tree.-----\n")
		outfile.close()
					
# Function Purpose: Delay the program until the reset time stamp
# Parameters: resetTimeStamp (The reset time stamp), simple (Shows complexity of the delay)
# Throws: None
# Return: timeToDelay (The amount of time the program will be delayed)
	
def delayCall(resetTimeStamp, simple=1):	

	if (simple == 1):
		print("Your program will be delayed by: 500 seconds.")
		time.sleep(500)
		return 500
	currentTime = calendar.timegm(time.gmtime())   
	timeToDelay = resetTimeStamp - currentTime     # The difference will constitute as the delay
	timeToDelay += 100       # Add an hour buffer to not anger the API :)
	print("Your program will be delayed by: ", timeToDelay, " seconds.")
	time.sleep(timeToDelay)
	return timeToDelay

# Function Purpose: Check the limits to ensure the user is not exceeding certain limits
# Parameters: simple (Shows complexity of the delay)
# Throws: None
# Return: None

def checkLimit(simple=1):

	if reddit.auth.limits['remaining'] <= 50:
		print("CAUTION! Reddit limit is below 100 at: ", reddit.auth.limits['remaining'])
		print("The Reddit time stamp is at: ", reddit.auth.limits['reset_timestamp'])
		print("The number of requests used: ", reddit.auth.limits['used'])
		printReport(begRunTime)
		delayCall(reddit.auth.limits['reset_timestamp'], simple)		

def createPostString(redditPost):
	
	postString = ''       # Create a string to write to a text file
	postString += redditPosts.id + '\t'   # Add the reddit id tag
	postString += '\'' + redditPosts.title + '\'' + '\t'    # Add the comment title to the final string
	postString += str(redditPosts.author)	+ '\t'  # Add the comment author to the final string 
	postString += str(redditPosts.created) + '\t'  # Add the time stamp to the final string
	postString += str(redditPosts.num_comments) + '\t'  # Add the comment number to the final string
	postString += str(redditPosts.num_crossposts) + '\t'  # Add the crossposts number to the final string
	postString += str(redditPosts.ups) + '\n'   # Add the upvote Numbers to the final string
	return postString

# Function Purpose: Create a string that outlines the attributes of a Reddit comment
# Parameters: redditCommentTree (The Reddit comment tree)
# Throws: None
# Return: commentString (The final string to be inserted in the text file)

def createCommentString(redditCommentTree):
	commentString = ''      # Repeat the same process as stated above
	commentString += comment.id + '\t'
	commentbody = comment.body
	commentbody = commentbody.replace('\n', ' ')      # Remove new lines from Reddit comments to conserve space
	commentString += '\'' + commentbody + '\'' + '\t'     # Body represents the comment 
	commentString += str(comment.created) + '\t' 
	commentString += str(comment.author) + '\t'
	commentString += str(comment.ups) + '\n'
	return commentString

subreddit = reddit.subreddit(SUBREDDIT_NAME) 

for date in range(START_DATE, END_DATE, INTERVAL_TIME):
	print("Now Processing date: ", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(date)))
	# Loop through the selected time frame and acquire the comments
	subredditPosts = subreddit.submissions(date, (date + (INTERVAL_TIME - 1)))
	for redditPosts in subredditPosts:  
		postString = createPostString(redditPosts)
		writeToFile(postString, entering=1)
		try:
			redditComments = redditPosts.comments.list()    # Create a list class for the comment tree and iterate through each comment 
			for comment in redditComments:
				commentString = createCommentString(comment)
				writeToFile(commentString, entering=3)     # Neither passing nor entering the string
				numCommentsProcessed += 1
		except:
			commentsSkipped += 1
		writeToFile('\n', entering=0)          # Leave the comment tree and check the limit	
		numPostsProcessed += 1
		checkLimit(simple=1)
		
	print("We have finished processing date: ", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(date)), "  -----Undergoing Delay-----")
	print("The current limit is: ", reddit.auth.limits)
	time.sleep(DELAY_TIME)    # Delay the program to prevent limit excess
	checkLimit(simple=1)

printReport(begRunTime)