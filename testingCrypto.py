# Test
# Author: Michael Krakovsky
# Version 1.0
# Date: March 7, 2018

import sys
from RetrievingRedditPosts import redditPosts 
from ParsingTechniques import parsingQueries
import praw
import calendar
import time

START_DATE = 1501935226    # Create a beginning date and an end date 
END_DATE = 1521370279
INTERVAL_TIME = 86400 * 3
LIMIT_NUM = 200         # Indicates the number of reddit comments per request
DELAY_TIME = 10      # Seconds is the amount of time the program will be temporarily halted
FILENAME = 'C:\\Users\\micha\\Desktop\\zCashRedditContent.txt'

reddit = praw.Reddit(client_id= '',       # Create a reddit instance
						client_secret= '',
						username= '', 
						password= '', 
						user_agent= '')
					
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
		time.sleep(500)
		return 500
	currentTime = calendar.timegm(time.gmtime())   
	timeToDelay = resetTimeStamp - currentTime     # The difference will constitute as the delay
	timeToDelay += 100       # Add an hour buffer to not anger the API :)
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
		waitTime = delayCall(reddit.auth.limits['reset_timestamp'], simple)		
		print("Your program was be delayed by: ", waitTime, " seconds.")

def createPostString(redditPost):
	
	postString = ''       # Create a string to write to a text file
	postString += redditPosts.id + ','   # Add the reddit id tag
	postString += '\'' + redditPosts.title + '\'' + ','    # Add the comment title to the final string
	postString += str(redditPosts.author)	+ ','  # Add the comment author to the final string 
	postString += str(redditPosts.created) + ','  # Add the time stamp to the final string
	postString += str(redditPosts.num_comments) + ','  # Add the comment number to the final string
	postString += str(redditPosts.num_crossposts) + ','  # Add the crossposts number to the final string
	postString += str(redditPosts.ups) + '\n'   # Add the upvote Numbers to the final string
	return postString

# Function Purpose: Create a string that outlines the attributes of a Reddit comment
# Parameters: redditCommentTree (The Reddit comment tree)
# Throws: None
# Return: commentString (The final string to be inserted in the text file)

def createCommentString(redditCommentTree):
	commentString = ''      # Repeat the same process as stated above
	commentString += comment.id + ','
	commentbody = comment.body
	commentbody = commentbody.replace('\n', ' ')      # Remove new lines from Reddit comments to conserve space
	commentString += '\'' + commentbody + '\'' + ','     # Body represents the comment 
	commentString += str(comment.created) + ',' 
	commentString += str(comment.author) + ','
	commentString += str(comment.ups) + '\n'
	return commentString

subreddit = reddit.subreddit('zec') 
commentsPassed = 0      # Keeps track of the number of comments passed

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
		except:
			commentsPassed += 1
			print("ERROR: Attempt came while trying to process a comment.")
			print("The amount of comments skipped: ", commentsPassed)
		writeToFile('\n', entering=0)          # Leave the comment tree and check the limit	
		checkLimit(simple=1)
		
	print("We have finished processing date: ", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(date)))
	print("The current limit is: ", reddit.auth.limits)
	print("-----Undergoing Delay-----")
	time.sleep(DELAY_TIME)    # Delay the program to prevent limit excess
		
	checkLimit(simple=1)
