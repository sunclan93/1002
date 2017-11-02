import pprint
import json
import csv
import pandas as pd

def loadCountryCode(filename):
	with open(filename) as file:
		reader = csv.reader(file)
		countryCode = {}
		for line in reader:
			#print(line)
			countryCode[line[0]]=int(line[1])
	return countryCode

def load(filename):
	#Load the database
	with open(filename,"r",encoding="utf-8") as f:
		db=json.load(f)
	print("Total number of items:", len(db))
	return db

def jsonDump(db,filename):
	with open(filename,"w",encoding="utf-8") as f:
		json.dump(db,f)

def statistify(db):
	db2=[]
	for item in db:
		tmp={}
		tmp["_counter"]=item["_counter"]
		#print(tmp["_counter"])
		tmp["budget"]=item["budget"]
		tmp["revenue"]=item["revenue"]
		tmp["runtime"]=item["runtime"]
		tmp["crew"]=len(item["crew"])
		tmp["cast"]=len(item["cast"])
		if len(item["genres"])>=1:
			tmp["genre"]=item["genres"][0]["id"]
		else:
			tmp["genre"]=-1
		if len(item["production_countries"])>=1:
			tmp["country"]=countryCode[item["production_countries"][0]["iso_3166_1"]]
		else:
			tmp["country"]=-1
		if len(item["production_companies"])>=1:
			tmp["company"]=item["production_companies"][0]["id"]
		else:
			tmp["company"]=-1
		#tmp["trend"]
		#tmp["#view"]
		tmp["_info"]={"title":item["title"],"id":item["id"]}
		db2.append(tmp)
		#print(tmp)
	jsonDump(db2,"movieDbStat.json")
	data=[[d['_counter'], d['budget'], d['revenue'], d['runtime'], d['crew'], d['cast'], d['genre'], d['country'], d['company']] for d in db2]
	df=pd.DataFrame(data, columns=['_counter','budget','revenue','runtime','crew','cast','genre','country','company'])
	print(df)
	return [db, df]

def analysis(df):
	me=df.mean()

countryCode=loadCountryCode("iso_3166_1.csv")
db=load("movieDbClean.json")
[db, df]=statistify(db)

print("\nOne example of statistical purpose database:")
print(db[0])

analysis(df)