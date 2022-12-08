## Trevor Thomas
"""
The following script utilizes PySpark DataFrames to create an inverted index of Stack
Overflow posts grouped by their tags.  To see the same process using RDDs instead, 
see the other python file 'TrevorT_InvInd_RDD_script.py'.
"""

from pyspark.sql.functions import *
from pyspark.sql import SparkSession

import pyspark
import pandas as pd
import matplotlib.pyplot as plt

## Create SparkSession (SparkContext not necessary if not working with RDDs)
spark = SparkSession.builder.getOrCreate()

## Load data from HDFS into PySpark DataFrame
df_01 = spark.read.csv('hdfs://localhost:9000/stackOF/input/QR2.csv')

def df_mapreducer(df):
    """
    The df_mapreducer() function takes the original Stack Overflow data and fully converts it into
    the complete inverted index.  It accepts a DF object as an argument, strips it of the excess 
    punctuation while splitting the tag column into a list of tags, and names each column.  It then
    uses .select() to choose the columns to work with, uses explode() to create the one-to-one mapping 
    of tags and ids, and uses .groupBy() to group the ids by the tag column.  Finally, it uses .agg() to 
    convert the GroupedData object back into a DataFrame that will be the returned value.
    """
    x = df.withColumn('_c1', regexp_replace('_c1', '><', ';'))\
    .withColumn('_c1', regexp_replace('_c1', '<', ''))\
    .withColumn('_c1', regexp_replace('_c1', '>', ''))\
    .select(col('_c0').alias('id'), split(col('_c1'), ';').alias('Tags'))\
    .select(explode('Tags').alias('Tag'), 'id').groupBy('Tag')\
    .agg(collect_list('id').alias('ids'))
    return x

## Applies df_mapreducer() to the original DataFrame
df_02 = df_mapreducer(df_01)

## Converts the PySpark DataFrame into a pandas DataFrame and adds a column called 'length' that indicates how many post ids are associated with a tag
df_03 = df_02.toPandas()
df_03['length'] = df_03['ids'].str.len()

## Sorts the DataFrame by the number of ids associated with a tag
sorted_df = df_03.sort_values(by='length', ascending=False)

## Creates a bar chart of the top 25 tags with the post associated posts
sorted_df.iloc[0:25].plot(x = 'Tag', y = 'length', kind = 'bar')

## Saves the pandas DataFrame to a .csv file in the working directory
df_03.to_csv('TrevorT_Invertdex_DFrameoutput.csv')

## Displays the bar chart using matplotlib
plt.show()
