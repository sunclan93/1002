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
	for item in db:
		tmp={}
		tmp["_counter"]=item["_counter"]
		#print(tmp["_counter"])
		tmp["revenue"]=item["revenue"]
		if item["budget"]>0:
			tmp["budget"]=item["budget"]
			tmp["ROI"]=tmp['revenue']/tmp['budget']
		tmp["runtime"]=item["runtime"]
		tmp["crew"]=len(item["crew"])
		tmp["cast"]=len(item["cast"])
		#print(type(tmp['cast']))
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
	#data=[[d['_counter'], d['budget'], d['revenue'], d['runtime'], d['crew'], d['cast'], d['genre'], d['country'], d['company']] for d in db2]
	df=pd.DataFrame(db2, columns=['_counter','budget','revenue','ROI','runtime','crew','cast','genre','country','company'])
	return [db, df]

def analysis(df):
	#======================================================
	# 1.1.1 Statistical Analysis
	#======================================================
	print("Statistical Analysis:\n=================================")
	numericAttrColumns=['budget','revenue','ROI','runtime','cast','crew']
	means=df[numericAttrColumns].mean()
	mid=df[numericAttrColumns].median()
	stand=df[numericAttrColumns].std()
	print("Quantitative attributes:")
	print("\nMeans:"); print(means)
	print("\nMedian:"); print(mid)
	print("\nstd:"); print(stand)

	discreteAttrColumns=['genre','country','company']
	mode=df[discreteAttrColumns].mode().astype(int)
	print("\nCategorical attributes:")
	print("Mode:"); print(mode)

	#======================================================
	# 1.1.2 Outliers
	#======================================================
	outlierAnaly(df)

	#======================================================
	# 1.1.3 Binning
	#======================================================
	#print(df['ROI'].quantile(q=.95))
	#names=range(0,12)
	bins=[-1, 1, 2, 3, 4, 5, 6, 8, 15, 1000, 10000000]
	df['Groups'] = pd.cut(df['ROI'], bins)
	print("\nBins and binning results:")
	print(df['Groups'].value_counts())

	#======================================================
	# 1.2.1 Histograms
	#======================================================
	pd.DataFrame(df['budget']).hist()
	plt.title("Histogram on budget")
	plt.savefig('histoBudget.png')

	pd.DataFrame(df['revenue']).hist()
	plt.title("Histogram on revenue")
	plt.savefig('histoRevenue.png')

	pd.DataFrame(df['runtime']).hist()
	plt.title("Histogram on runtime")
	plt.savefig('histoRuntime.png')

	#======================================================
	# 1.2.2 Correlations
	#======================================================
	columns=['budget','revenue','runtime']
	print("\nCorrelations\n=================================")
	print(df[columns].corr())
	pd.plotting.scatter_matrix(df[columns])
	plt.title("Scatter Matrix on budget, revenue and runtime")
	plt.savefig('scatter.png')

	#======================================================
	# 1.3.1 Clusters
	#======================================================
	from sklearn import cluster
	from sklearn.preprocessing import normalize

	# Normalization
	columns=['budget','revenue','ROI','runtime','crew','cast','genre','country','company']
	array = df[columns].dropna().as_matrix()
	arrayp = normalize(array,axis=0,norm='l2')

	clusterHi=cluster.AgglomerativeClustering(n_clusters=3)
	clusterKM=cluster.KMeans(n_clusters=3)
	clusterDB=cluster.DBSCAN(eps=0.03)

	clusterHi.fit(arrayp)
	clusterKM.fit(arrayp)
	clusterDB.fit(arrayp)

	y=[]
	y.append(clusterHi.fit_predict(arrayp))
	y.append(clusterKM.fit_predict(arrayp))
	y.append(clusterDB.fit_predict(arrayp))

	#======================================================
	# 1.3.2 Silhouette Coeff.
	#======================================================
	from sklearn import metrics

	print("\nSilhouette Coeff.\n=================================")
	for i, name in enumerate(['Hierarchical','KMeans','dbScan']):
		print(name,' ',metrics.silhouette_score(arrayp, y[i], metric='euclidean'))

	fig = plt.figure(1, figsize=(4, 3))
	for i, name in enumerate(['Hierarchical','KMeans','dbScan']):
		plotPCA(arrayp,y[i],name)

def plotPCA(X,y,name):
	from sklearn import decomposition

	plt.clf(); plt.cla()
	pca = decomposition.PCA(n_components=2)
	pca.fit(X)
	X = pca.transform(X)

	for i, color in enumerate(['red','blue','green']):
		plt.scatter(X[y==i,0],X[y==i,1],c=color,label=name+': '+str(np.sum(y==i))+' itmes',edgecolors='black')
	if -1 in y:
		plt.scatter(X[y==-1,0],X[y==-1,1],c='black',label='outliers: '+str(np.sum(y==-1))+' items',edgecolors='black')
	
	plt.title('Cluster PCA projection: '+name)
	plt.legend()
	plt.grid(True)
	plt.savefig('clusterPCA'+name+'.png')

def outlierAnaly(df):
	plt.clf(); plt.cla()
	pd.DataFrame(df['ROI']).boxplot()
	plt.title("Box plots on ROI")
	plt.savefig('boxPlotROI.png')

	plt.clf(); plt.cla()
	pd.DataFrame(df['runtime']).boxplot()
	plt.title("Box plots on runtime")
	plt.savefig('boxPlotRuntime.png')

def LOF(df):
	columns=['_counter','budget','revenue','ROI','runtime','crew','cast','genre','country','company']
	array=df[columns].dropna().as_matrix()
	print("\nOutlier:\n=================================")
	clf=LocalOutlierFactor(n_neighbors=50, contamination=0.004)
	y_pred = clf.fit_predict(array[:,1:])
	otlr=[]
	for i, p in enumerate(y_pred):
		if p == -1:
			otlr.append(int(array[i,0]))
	print("Number of outliers: ",len(otlr))
	print("\nLabel of outliers:")
	print(otlr)
	print("\nTitle of outliers:")
	for i in otlr:
		for item in db:
			if item['_counter']==i:
				print(item['title'])

if __name__=="__main__":
	countryCode=loadCountryCode("iso_3166_1.csv")
	db=load("movieDbClean.json")
	[db, df]=quantify(db,countryCode)

	analysis(df)

	LOF(df)
