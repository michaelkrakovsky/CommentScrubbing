# Author: Michael Krakovsky
# Date: March 29, 2018
# Version 0.1
# Description: The program will take a text file, convert to a pandas database and run sentiment analysis on it
# Posts are formatted in the following way: id, title, author, date, comment Number, crosspost Number, ups, Post Flag
# Comments are formatted in the following way: id, body, created, author, ups, Post Id
# Finally, all of the arrays will be stored in a pickle file

import nltk
import glob
import pickle 

FILENAME = r"C:\Users\micha\Dropbox\RedditComment\SubredditThreads\0xProjectClean.txt"

# Description: Open File to and return a 1D array containing reddit posts and comments (unstructured)
# Parameters: fileName (Name of the file)
# Throws: None
# Returns: content (An array containing the data)

def openFile(fileName):

	with open(fileName, encoding='utf8') as file:   #Read the file contents into a list
		content = file.readlines()	
	return content
	
# Description: Iterate through a single array element and separate the content based on apostrophe and comma locations.
# Since the data is unstructured, we need to ignore certain aspects of the data such as apostrophes in between apostrophes 		
# Parameters: line (The line that requires editing)
# Throws: None
# Return: sortedLine (A new line element that sorts the contents within the array)

def organiseSingleLine(line):

	inApostrophe = False      # Indicates whether we are within the string. This is used to treat commas differently depending on where we are.
	string = ""				  # Buffer used to temporarily store the string
	sortedLine = []
	
	for idx, val in enumerate(line):
		if (val != '\n'):
			if (val == '\''):
				if ((line[idx - 1] == ',') and (line[idx + 1] == ",")):
					inApostrophe = False
				elif (line[idx - 1] == ','):
					inApostrophe = True
				elif ((line[idx + 1] == ',') and (line[idx + 2] != " ")):
					inApostrophe = False
			if (val == ','):
				if (inApostrophe == True):
					string += val
				else:
					sortedLine.append(string)
					string = ""
			else:
				string += val
	sortedLine.append(string.rstrip())       # Add the last character to the array since there is no comma afterwards
	return sortedLine
	
# Description: Enumerate throw every line within the array of reddit contents
# Parameters: redditArray (The array containing reddit posts and comments)
# Throws: None
# Returns: sortedArray (The final two 2D array with the organised content), missedContent (An integer indicating the number of posts skipped over)

def organiseData(subRedditContent, printMissedContent=0):
	
	sortedArray = []
	missedContent = 0 
	lineContent = None
	
	for index, line in enumerate(subRedditContent): 
		lineContent = organiseSingleLine(line)
		if ((len(lineContent) != 6) and (len(lineContent) != 8)):      # Append to array if the element is good, otherwise do not and update counter
			missedContent += 1
		else:
			sortedArray.append(lineContent)
	if (printMissedContent != 0):
		print("The ammount of missed content skipped was: ", missedContent)
	return sortedArray
	

for fileName in glob.iglob('C:\\Users\\micha\\Dropbox\\RedditComment\\SubredditThreads\\*.txt'):        # Iterate throw all the file names in the directory
	fileContent = openFile(fileName)     # Get the contents of the file and store it in an array
	sortedArray = organiseData(fileContent)
	
	fileNameToWrite = fileName[0:-4]     # Remove the ending of the file name
	fileNameToWrite += "PickleVersion.pickle"
	
	fileToDump = open(fileNameToWrite, "wb")  # Dump the file to a pickle file
	pickle.dump(sortedArray, fileToDump)
	fileToDump.close()
	
print("All text files have been put into a pickle file and are ready.")
