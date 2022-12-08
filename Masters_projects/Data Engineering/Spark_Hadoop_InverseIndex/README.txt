This directory contains the final project for my Data Engineering course.  The purpose of the project was to build an inverse index of Stack Overflow posts based on their tags using HDFS as the file system and Spark as the MapReducer.  I completed the project twice using two Spark data structures - the original RDD and the newer Dataframe - to compare the differences between the two. 

*Note - I've intentionally left the project as a series of scripts and text documents rather than adapting it to a Notebook for ease of viewing.  This is because I have other examples of utilizing Notebooks in my portfolio and wanted to showcase to potential employers my comfort scripting in terminal shells and writing results to documents without immediate interpreter feedback.

The contents of the directory are as follows, with a brief description after each item:

 - Original_StackOF_Data.csv - data obtained from data.stackexchange.com
 - StackOF_SQL_query.sql - SQL query used on data.stackexchange.com database to obtain above file
 - Trevor_Thomas_FinalProject_InvertedIndex.pdf - full writeup on process and results with code
 - TrevorT_Invertdex_DFrameoutput.csv - final output from the project using Dataframe data object
 - TrevorT_Invertdex_RDDoutput.csv - final output from the project using RDD data object
 - TrevorT_InvInd_DataFrame_script.py - script ran to complete the project using Dataframe object
 - TrevorT_InvInd_RDD_script.py - script ran to complete the project using RDD object


