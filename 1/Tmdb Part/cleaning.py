#In this script, we clean the movie database we collected.
#The standard we use is basically the same as we used in cleanliness part.
import json
import pprint
from cleanliness import load, removeUseless

if __name__ == "__main__":
	db=load()

	counter = 0
	db2=[]
	totalCasts = 0
	totalCrews = 0
	#We clean the dataset by following steps:
	for item in db:
		if item['homepage']=='':									#unify the format of blank homepage as None
			item['homepage']==None
		if item['revenue']<0:										#remove items with no revenue information
			continue
		if item['runtime']==None:									#remove items with no length information
			continue
		elif item['runtime']<=30:									#disqualify items as movies with short runtime by removing them
			continue
		if item['spoken_languages']==[]:							#if the movie has no spoken languages,
			if item['original_language']!=[]:						#consider the original language as one of its languages (if exists)
				item['spoken_languages']=item['original_language']
		if item['title']=='':										#remove items with no title
			continue
		totalCasts += len(item['cast'])
		totalCrews += len(item['crew'])
		db2.append(item)
	aveCast = totalCasts/len(db)
	aveCrew = totalCrews/len(db)

	db = []
	counter = 0
	with open("movieList.csv","w",encoding='utf-8') as f:
		f.write(",id,title\n")
		for item in db2:												#and remove items with few credits information
			if len(item['cast'])<aveCast/4:
				continue
			if len(item['crew'])<aveCrew/8:
				continue
			item['_counter'] = counter
			counter += 1
			db.append(item)
			#write the movie title into the movie list
			f.write(str(counter))
			f.write(',')
			f.write(str(item['id']))
			f.write(',')
			f.write(item['title'])
			f.write(",\n")
	with open("movieDbClean.json","w",encoding="utf-8") as f:
		json.dump(db,f)
	print("New total number:", len(db))
