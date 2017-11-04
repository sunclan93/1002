import pprint
import json
import csv
import pandas as pd
import numpy as np
from sklearn.neighbors import LocalOutlierFactor
import matplotlib.pyplot as plt

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

def quantify(db,countryCode):
	db2=[]
	test=[]
	for item in db:
		tmp={}
		tmp["_counter"]=item["_counter"]
		#print(tmp["_counter"])
		tmp["revenue"]=item["revenue"]
		if item["budget"]>0:
			tmp["budget"]=item["budget"]
			tmp["ROI"]=tmp['revenue']/tmp['budget']
			#if tmp["ROI"]>=1000:
			#	continue;
		tmp["runtime"]=item["runtime"]
		tmp["crew"]=len(item["crew"])
		tmp["cast"]=len(item["cast"])
		print(type(tmp['cast']))
		if len(item["genres"])>=1:
			tmp["genre"]=item["genres"][0]["id"]
			if (type(tmp['genre']) not in test):
				test.append(type(tmp['genre']))
		#else:
		#	tmp["genre"]=-1
		if len(item["production_countries"])>=1:
			tmp["country"]=countryCode[item["production_countries"][0]["iso_3166_1"]]
		#else:
		#	tmp["country"]=-1
		if len(item["production_companies"])>=1:
			tmp["company"]=item["production_companies"][0]["id"]
		#else:
		#	tmp["company"]=-1
		#tmp["trend"]
		#tmp["#view"]
		tmp["_info"]={"title":item["title"],"id":item["id"]}
		db2.append(tmp)
		#print(tmp)
	jsonDump(db2,"movieDbStat.json")
	#data=[[d['_counter'], d['budget'], d['revenue'], d['runtime'], d['crew'], d['cast'], d['genre'], d['country'], d['company']] for d in db2]
	df=pd.DataFrame(db2, columns=['_counter','budget','revenue','ROI','runtime','crew','cast','genre','country','company'])
	print(df)
	print(test)
	return [db, df]

def analysis(df):
	#means=[]
	#means.append(df['budget'].mean())
	#means.append(df['revenue'].mean())
	#means.append(df['runtime'].mean())
	#means.append(df['cast'].mean())
	#means.append(df['crew'].mean())
	#means=pd.DataFrame([means], columns=['budget','revenue','runtime','cast','crew'])
	numericAttrColumns=['budget','revenue','ROI','runtime','cast','crew']
	means=df[numericAttrColumns].mean()
	mid=df[numericAttrColumns].median()
	stand=df[numericAttrColumns].std()
	print(means, '\n', mid,'\n',stand)

	discreteAttrColumns=['genre','country','company']
	mode=df[discreteAttrColumns].mode().astype(int)
	print(mode)

	#print(df['ROI'].quantile(q=.95))
	#names=range(0,12)
	bins=[-1, 1, 2, 3, 4, 5, 6, 8, 10, 15, 20, 30, 100]
	df['Groups'] = pd.cut(df['ROI'], bins)
	print(df['Groups'].dtype)


def outlierAnaly(df):
	pd.DataFrame(df['ROI']).boxplot()
	plt.title("Box plots of all variables in data set")
	plt.savefig('boxPlotBudget.png')

def LOF(df):
	columns=['_counter','budget','revenue','ROI','runtime','crew','cast','genre','country','company']
	array=df[columns].dropna().as_matrix();
	print(len(array))
	clf=LocalOutlierFactor(n_neighbors=50, contamination=0.004)
	y_pred = clf.fit_predict(array[:,1:])
	otlr=[]
	for i, p in enumerate(y_pred):
		if p == -1:
			otlr.append(array[i,0])
	print(otlr)
	for i in otlr:
		for item in db:
			if item['_counter']==i:
				print(item['title'])
	print(len(otlr))

if __name__=="__main__":
	countryCode=loadCountryCode("iso_3166_1.csv")
	db=load("movieDbClean.json")
	[db, df]=quantify(db,countryCode)

	analysis(df)

	outlierAnaly(df)

	LOF(df)
