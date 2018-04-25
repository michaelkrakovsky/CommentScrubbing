# File Description: A script to put all dictionaries into a csv file.
# Author: Michael Krakovsky
# Version 1.0
# Date: April 15, 2018

import pickle 
import pandas as pd
import time
import os

DIRECTORY_TO_ANALYSE = r"C:\Users\micha\Dropbox\RedditComment\PushShift_Weighted_Scores"
FILE_TO_WRITE = r"C:\Users\micha\Dropbox\RedditComment\PushShift_Weighted_Scores_XLSX\Weighted_Sentiment.xlsx"
directory = os.fsencode(DIRECTORY_TO_ANALYSE)

# Function Description: Load a previously created pickle file
# Parameters: fileName (The name of the file), initialDir (The name of the directory where the file is located)
# Throws: None
# Return: content (The content within the pickle file)
	
def loadAPickleFile(fileName, initialDir):

	file = open(initialDir + "\\" + fileName, "rb")		# Complete pickling procedure
	content = pickle.load(file)
	file.close()
	return content

# Function Purpose: Convert a tuple of four dictionaries of the same indexes into one DataFrame
# Parameters: dicts (The tuple with the four dicts)
# Throws: None
# Returns concatDataFrame (The combination of the DataFrames)

def dictsToOneDataframe(dicts):
	
	if (len(dicts) != 4):
		raise ValueError("The size of the tuple is not equal to 4")
	
	dfOne = pd.DataFrame(list(dicts[0].items()))				# Create a DataFrame from each dictionary
	dfTwo = pd.DataFrame(list(dicts[1].items()))
	dfThree = pd.DataFrame(list(dicts[2].items()))
	dfFour = pd.DataFrame(list(dicts[3].items()))
	
	dfOne.columns = ['Date', 'Weighted_Score']			# Title each column of each DataFrame appropriately
	dfTwo.columns = ['Date', 'Num_Comments_in_Day']
	dfThree.columns = ['Date', 'Num_Posts_in_Day']
	dfFour.columns = ['Date', 'Total_Score_in_Day']
	
	dfOne = dfOne.set_index('Date')						# Set the date as the index for each DataFrame 
	dfTwo = dfTwo.set_index('Date')
	dfThree = dfThree.set_index('Date')
	dfFour = dfFour.set_index('Date')
	
	concatDataFrame = pd.concat([dfOne, dfTwo, dfThree, dfFour], axis=1)		# Concatenate the DataFrame into one 
	concatDataFrame = concatDataFrame.fillna(0)			# Fill the NaN values with 0
	concatDataFrame.reset_index(level=0, inplace=True)			# Ensure the date is now its own column 
	concatDataFrame['Date_In_Readable'] = concatDataFrame.apply(lambda row: time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(row['Date'])), axis=1)   # Convert into readable time
	concatDataFrame['Total_Traffic_In_Day'] = concatDataFrame.apply(lambda row: row['Num_Comments_in_Day'] + row['Num_Posts_in_Day'], axis=1)			# Find the total number of traffic in the day
	concatDataFrame['Sentiment_Mult_Traffic'] = concatDataFrame.apply(lambda row: row['Total_Traffic_In_Day'] * row['Weighted_Score'], axis=1)				# Find the weighted score in the day
	concatDataFrame = concatDataFrame[['Date', 
										'Date_In_Readable', 
										'Weighted_Score', 
										'Num_Comments_in_Day', 
										'Num_Posts_in_Day', 
										'Total_Traffic_In_Day', 
										'Sentiment_Mult_Traffic']]		# Hard code the order of the columns for better readability
	return concatDataFrame				

writer = pd.ExcelWriter(FILE_TO_WRITE)
for file in os.listdir(directory):					# Loop through all the files in the entire directory
	
	fileName = os.fsdecode(file)					# Stores only the file name
	content = loadAPickleFile(fileName, DIRECTORY_TO_ANALYSE)    				# Load the pickle file into the dictionary
	print(fileName)
	df = dictsToOneDataframe(content)				# Convert the dictionaries to a dataFrame
	df.to_excel(writer, fileName[15:-12])

writer.save()										# Save the excel file