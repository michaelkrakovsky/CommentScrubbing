# Description: The following object will create queries.
# Arguments: None 
# Author: Michael Krakovsky
# Version 1.0
# Date: March 9, 2018

import praw

class redditPosts:

    # Description: Initializing method
	# Parameters: (1) numPosts (Number of posts needed) Must be greater than 0, 
	# less than 101, and of type int (2) postType (What section the posts come from)
	# Must match be one of the following: 'H' (HOT) 'N'(NEW) 'R'(RISING) 'T' (TOP) 
	# (3) subredditObject (A subreddit object)
	
	def __init__(self):
	    pass
		
	def createQuery(self, num, post, sub):
		if ((isinstance(num, int) == False) or (num < 1) or (num > 5000)):
			raise ValueError("Error: The number of posts you submitted is invalid.")
		elif (isinstance(sub, praw.models.reddit.subreddit.Subreddit) == False):
			raise ValueError("Error: Your subreddit instance is invalid")
		elif (post == 'H'):
			return sub.hot(limit=num)
		elif (post == 'N'):
			return sub.new(limit=num)
		elif (post == 'R'):
			return sub.rising(limit=num)
		elif (post == 'T'):
			return sub.top(limit=num)
		else:
			raise ValueError("Error: The post type you have entered is incorrect.")			
    
		


