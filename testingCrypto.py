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
DELAY_TIME = 20      # 90 Seconds is the amount of time the program will be temporarily halted

reddit = praw.Reddit(client_id= '',       # Create a reddit instance
						client_secret= '',
						username= '', 
						password= '', 
						user_agent= '')
					
# Function Purpose: Delay the program until the reset time stamp
# Parameters: The reset time stamp
# Throws: None
# Return: timeToDelay (The amount of time the program will be delayed)
	
def delayCall(resetTimeStamp):	

	currentTime = calendar.timegm(time.gmtime())   
	timeToDelay = resetTimeStamp - currentTime     # The difference will constitute as the delay
	timeToDelay += 3600       # Add an hour buffer to not anger the API :)
	time.sleep(timeToDelay)
	return timeToDelay

subreddit = reddit.subreddit('NEO') 
commentsPassed = 0      # Keeps track of the number of comments passed

for date in range(START_DATE, END_DATE):
	# Loop through the selected time frame and acquire the comments
	for redditPosts in subreddit.submissions(date, (date + INTERVAL_TIME)):    
		postString = ''       # Create a string to write to a text file
		postString += redditPosts.id + ','   # Add the reddit id tag
		postString += '\'' + redditPosts.title + '\'' + ','    # Add the comment title to the final string
		postString += str(redditPosts.author)	+ ','  # Add the comment author to the final string 
		postString += str(redditPosts.created) + ','  # Add the time stamp to the final string
		postString += str(redditPosts.num_comments) + ','  # Add the comment number to the final string
		postString += str(redditPosts.num_crossposts) + ','  # Add the crossposts number to the final string
		postString += str(redditPosts.ups) + '\n'   # Add the upvote Numbers to the final string

		# Write the created string into the text file
		with open('C:\\Users\\micha\\Desktop\\NeoRedditContent.txt', "a", encoding='utf8') as outfile:
			outfile.write(postString)
			outfile.write("-----Entering the comment tree.-----\n")
			outfile.close()
		try:
			redditComments = redditPosts.comments.list()    # Create a list class for the comment tree and iterate through each comment 
			for comment in redditComments:
				commentString = ''      # Repeat the same process as stated above
				commentString += comment.id + ','
				commentbody = comment.body
				commentbody = commentbody.replace('\n', ' ')      # Remove new lines from Reddit comments to conserve space
				commentString += '\'' + commentbody + '\'' + ','     # Body represents the comment 
				commentString += str(comment.created) + ',' 
				commentString += str(comment.author) + ','
				commentString += str(comment.ups) + '\n'
				
				with open('C:\\Users\\micha\\Desktop\\NeoRedditContent.txt', "a", encoding='utf8') as outfile:
					outfile.write(commentString)
					outfile.close()
		except:
			commentsPassed += 1
			print("ERROR: Attempt came while trying to process a comment.")
			print("The amount of comments skipped: ", commentsPassed)
			
			# Delay if the program if the limits are about to be reached
			if reddit.auth.limits['remaining'] <= 5:
				print("CAUTION! Reddit limit is below 100 at: ", reddit.auth.limits['remaining'])
				print("The Reddit time stamp is at: ", reddit.auth.limits['reset_timestamp'])
				print("The number of requests used: ", reddit.auth.limits['used'])	
				waitTime = delayCall(reddit.auth.limits['reset_timestamp'])
				print("Your program will be delayed by: ", waitTime, " seconds.")
			
		# Indicate the exit of the comment tree
		with open('C:\\Users\\micha\\Desktop\\NeoRedditContent.txt', "a", encoding='utf8') as outfile:
			outfile.write("-----Exiting the comment tree.-----\n")
			outfile.close()
		
		print("We have finished processing date: ", time.('%Y-%m-%d %H:%M:%S', time.localtime(date)))
		print("The current limit is: ", reddit.auth.limits)
		print("-----Undergoing Delay-----")
		date += INTERVAL_TIME     # Shift the counter forward
		time.sleep(DELAY_TIME)    # Delay the program to prevent limit excess
		print("Now Processing date: ", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime((date + INTERVAL_TIME))))
		
		# Delay if the program if the limits are about to be reached
		if reddit.auth.limits['remaining'] <= 25:
			print("CAUTION! Reddit limit is below 100 at: ", reddit.auth.limits['remaining'])
			print("The Reddit time stamp is at: ", reddit.auth.limits['reset_timestamp'])
			print("The number of requests used: ", reddit.auth.limits['used'])
			waitTime = delayCall(reddit.auth.limits['reset_timestamp'])		
			print("Your program will be delayed by: ", waitTime, " seconds.")
		

