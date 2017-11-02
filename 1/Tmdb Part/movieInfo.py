#In this script, we collect information of movies between 2005 through 2017 (or today).
#For the purpose of our study, we only collect movies released in the US
import numpy
import pandas as pd
from pprint import pprint

import time

import requests
from urllib.error import URLError, HTTPError

import json

def findMovieByYear(year):
	#In this function, we fetch 'id's of movies of certain year, and return them as a list
	#The form of query and response can be found at "https://developers.themoviedb.org/3/discover"
	baseURL = "https://api.themoviedb.org/3/discover/movie?api_key=98c32aa3e98b8f1a0041e3ecff9f0624"
	urlPost = {
		'language' : 'en-US',
		'region' : 'US',
		'sort_by' : 'release_date.asc', 
		'include_adult' : 'false',
		'include_video' : 'false',
		'primary_release_year' : str(year),
		'page' : '1'
	}
	page = 1 #The results of a quest comes as a set of pages. In every page there are no more than 20 movies.
	while True:
		response=requests.get(baseURL,urlPost)
		if response.status_code!=200:
			print(response.status_code)
			time.sleep(8)  #The site requires no more than 40 requests in 10 seconds, or it will give a 429 error.
		else:
			break
	result=response.json()
	while (int(result['total_pages'])>=page):
		for items in result['results']:
			if items['release_date']<today and (items['id'] not in idList):
				idList.append(items['id'])
		page += 1
		urlPost['page'] = page
		while True:
			response=requests.get(baseURL,urlPost)
			if response.status_code!=200:
				print(response.status_code)
				time.sleep(8)
			else:
				break
		result=response.json()
		#print(result['page'],result['total_pages'])

def getMovie(idList):
	#In this function, we use the idList to collect necessary information about the movies
	#The information we need are stored separately in two places: general informatoins or "details", and credits.
	#The form of query and response of "details" can be found at "https://developers.themoviedb.org/3/movies"
	#The form of query and response of "details" can be found at "https://developers.themoviedb.org/3/movies/get-movie-credits"
	counter = 0
	print(idList)
	for item in idList:
		baseURL = "https://api.themoviedb.org/3/movie/" + str(item) +"?api_key=98c32aa3e98b8f1a0041e3ecff9f0624&language=en-US"
		while True:
			response=requests.get(baseURL)
			if response.status_code!=200:
				print(response.status_code)
				time.sleep(8)
			else:
				break
		result = response.json()
		baseURL = "https://api.themoviedb.org/3/movie/" + str(item) +"/credits?api_key=98c32aa3e98b8f1a0041e3ecff9f0624"
		while True:
			response=requests.get(baseURL)
			if response.status_code!=200:
				print(response.status_code)
				time.sleep(8)
			else:
				break
		result1 = response.json()
		result['cast'] = result1['cast']
		result['crew'] = result1['crew']
		result['_counter'] = counter;
		#print(counter,result['id'],result['title'])
		counter += 1
		#write the information into .json
		with open("db.json","a",encoding='utf-8') as f:
			json.dump(result,f)
			f.write(",") #Note: For the very last item, it will still be followed by ',' but not ']'. Will correct that using correctForm()
	print(len(idList), "One Year Finished")

def correctForm(a1,a2):
	with open(a1,"r") as f1, open(a2,"w") as f2:
		a=f1.read(1)
		b=f1.read(1)
		while b!="":
			f2.write(a)
			a=b
			b=f1.read(1)
		f2.write(']')
	import shutil, os
	os.unlink(a1)
	shutil.move(a2,a1)

if __name__=="__main__":
	#Create a head of the .json file
	with open("db.json","w") as f:
		f.write("[")

	#Find movies by year and pull the possibly needed information
	today = time.strftime('%Y-%m-%d',time.localtime(time.time()))
	for i in range(2005,2018):
		idList = []
		print("getting", i)
		findMovieByYear(i)
		getMovie(idList)

	#Correct the format of .json file
	correctForm("db.json","db2.json")
