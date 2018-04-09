# Author: Michael Krakovsky
# Date: March 26, 2018
# Version 0.1
# Description: The program will take custom made Reddit scrubbing txt files and clean the data up. Some of these functions include:
# 1. Removing tags (labeled with <>)
# 2. Removing empty spaces
# 3. Adding a flag to each line indicating '1' a post or 'POSTID' a comment
# 4. Adding the post id to all comments belonging to that specific post

import glob

inPost = False

# Description: Retrieve the post id from a reddit post. Assume the id is the first input.
# Parameters: line (The reddit Post)
# Throws: None
# Return: postId (The id from the reddit post)

def scrubForPostId(line):
	postId = ""
	i = 0
	while line[i] != ',':
		postId += line[i]
		i += 1
	return postId

# Description: Create a new file with the appropriate name
# Parameters: fileName (The original file name)
# Throws: None
# Return: fileNameToWrite (The name of the file name that was written)

def createNewFile(fileName):
	fileNameToWrite = fileName[0:-4]     # Remove the ending of the file name
	fileNameToWrite += "Clean.txt"
	f = open(fileNameToWrite, "w+")       # 'w+' create a new file
	f.close()
	return fileNameToWrite
	
for fileName in glob.iglob('C:\\Users\\micha\\Dropbox\\RedditComment\\SubredditThreads\\*.txt'):        # Iterate throw all the file names in the directory

	with open(fileName, encoding='utf8') as file:
		content = file.readlines()
		
	newList = [name for index, name in enumerate(content) if name != '\n']      # Remove all entries that only have a new line
	fileNameToWrite = createNewFile(fileName)
	postId = ""
	for line in newList:      
		stringToWrite = ''
		if (line == '-----Entering the comment tree.-----\n'):     # Detect whether you are in comment tree or not
			inPost = True
		elif (line == '-----Exiting the comment tree.-----\n'):
			inPost = False
		else:
			if (inPost == True):  			# Make changes to the lines 
				stringToWrite = line.replace("\n", "")
				stringToWrite += ',' + postId
				stringToWrite += '\n'
			else:
				postId = scrubForPostId(line)
				stringToWrite = line.replace("\n", "")
				stringToWrite += ',1'
				stringToWrite += '\n'
				
			with open(fileNameToWrite, "a", encoding='utf8') as outfile:
				outfile.write(stringToWrite)		
