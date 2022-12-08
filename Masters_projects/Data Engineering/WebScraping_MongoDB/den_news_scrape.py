import requests as req
import pandas as pd
from bs4 import BeautifulSoup as bs
from pymongo import MongoClient

## Initialize variables for MongoDB
client = MongoClient()
db = client['News']
collection = db['Den_Gov']
website = 'https://www.colorado.gov/news?page={}'

## Outer for loop that iterates through each page of website and saves the relevant content to variable "divs"
for i in range(81):
	website_f = website.format(i)
	page = req.get(website_f)
	clean_page = bs(page.content)
	divs = clean_page.find_all('div', {'class' : 'view-page-item'})

## Inner for loop the iterates through individual stories on each page, saving relevant info to database
	for d in divs:
		date = pd.to_datetime(d.find('div', {'class' : 'date margin-b'}).text)
		link = d.find('a')
		title = link.text
		address = link.get('href')

		collection.insert_one({'date' : date, 'URL' : address, 'title' : title})

## Closes MongoClient
client.close()
