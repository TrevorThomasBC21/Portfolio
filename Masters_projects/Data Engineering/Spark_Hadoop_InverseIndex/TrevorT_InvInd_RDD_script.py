"""
The following script utilizes PySpark RDDs to create an inverted index of Stack
Overflow posts grouped by their tags.  To see the same process using PySpark
DataFrames instead, see the other python file 'TrevorT_InvInd_DataFrame_script.py'.
"""
from pyspark.sql.functions import *
from pyspark import SparkContext
from pyspark.sql import SparkSession

import pandas as pd
import matplotlib.pyplot as plt

## Create SparkContext and SparkSession
sc = SparkContext().getOrCreate()
spark = SparkSession(sc)

## Load data from HDFS into RDD variable
rdd_01 = sc.textFile('hdfs://localhost:9000/stackOF/input/QR2.csv')

def cleaner(rdd):
    """ 
    The cleaner() function takes the original RDD and transforms it into a format that 
    can be MapReduced.  It strips the excess punctuation and symbols that came from the 
    original SQL query and splits the tag column into a list of the associated tags.  It 
    returns the cleaned data still in type RDD.
    """
    j = rdd.map(lambda i: i.split(','))
    x = j.map(lambda k: (k[1].replace('><', ';')\
    .replace('<', '')\
    .replace('>', '')\
    .replace('"', ''), k[0].replace('"', '')))
    z = x.map(lambda r: (r[0].split(';'), r[1]))
    return z

def mapper(iter):
    """
    The mapper() function takes an RDD and iterates through it to create a one-to-one
    mapping of tags and post ids.  It creates an empty list, turns the RDD into an 
    iterable object, and goes through each individual element with a for loop.  With another
    nested for loop, it iterates through the list of tags and appends them to the empty list
    one by one with their associated post id as a key*value pair.  It returns another RDD.
    """
    op = []
    iter = iter.collect()
    for i in iter:
        for p in range(len(i[0])):
            op.append((i[0][p], i[1]))
    rdd = sc.parallelize(op)
    return rdd

def reducer(mapped):
    """
    The reducer() function takes an RDD that has already been mapped and groups it by the tag column.
    It returns another RDD made of key*value pairs, where the key is the tag and the value is a list
    of the post ids associated with said tag.
    """
    x = mapped.groupByKey().map(lambda j: (j[0], list(j[1])))
    return x

## Applies all three functions to the original RDD to return the inverted index as an RDD
rdd_02 = reducer(mapper(cleaner(rdd_01)))

## Transforms inverted index from RDD into PySpark DataFrame and then to pandas DataFrame
pand_df = rdd_02.toDF().toPandas()

## Exports pandas DataFrame to a .csv file in working directory
pand_df.to_csv('TrevorT_Invertdex_RDDoutput.csv')
