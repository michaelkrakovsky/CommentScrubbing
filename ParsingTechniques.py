# Description: The following object will perform adjustments on reddit queires.
# Arguments: None
# Author: Michael Krakovsky
# Version 1.0
# Date: March 10, 2018

import praw

class parsingQueries:
	
	# Class Variables: query (Stores the subreddit query to effectively parse through the content)
	
	query = None
			
	# Initiator: The object will accept a query Post
	# Parameter: queryPost (Query of reddit comments)
	# Throws: None
	# Return: None
	
	def __init__(self, queryPost):
		self.query = queryPost
	
	# Function Purpose: Ensures the type is praw.models.listing.generator.ListingGenerator
	# Parameters: queryPost (Query of reddit comments)
	# Throws: TypeError (When type inputted is wrong)
	# Return: None
	
	def ensureType(self):
		if(isinstance(self.query, praw.models.listing.generator.ListingGenerator) == False):
			raise TypeError("You have failed to enter a query")
	
	# Function Purpose: Returns a list containing post titles
	# Parameter: None
	# Throws: TypeError (When type is inputted is wrong)
	# Return: postTitleList (List of posts title)
	
	def queryPostNames(self):
		
		postTitleList = []
		
		#parsingQueries.ensureType(self)
		for submission in self.query:
			postTitleList.append(submission.title)
		return postTitleList
		
	# Function Purpose: Returns a list containing all elements of the specified query
	# Parameter: None
	# Throws: TypeError (When type is inputted is wrong)
	# Return: postList (List of specified posts)
	
	def queryPosts(self):
		
		postList = []
		
		parsingQueries.ensureType(self)
		
	
	
		
	