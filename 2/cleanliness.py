#In this script, we test the cleanliness of the movie database we collected
#We calculate number of "bad" (as defined in following parts) attributes on items and print it.
#For all attributes we examined, the smaller the amount of bad items is, the better the attribute is.
import json
import pprint

def removeUseless(db):
	#We intend to study (or predict) movie's revenue, so if the movie has no 
	#revenue information, we choose to remove it from the database.
	counter = 0
	db2 = []
	for item in db:
		if item['revenue']!=0:
			counter += 1
			item['_counter']=str(counter)
			db2.append(item)
	return db2

def load(filename):
	#Load the database
	with open(filename,"r",encoding="utf-8") as f:
		db=json.load(f)
	print("Total number of items in origin database:", len(db))
	#Remove items that will not contribute to our study
	db=removeUseless(db)
	print("Total number of items:", len(db))
	return db

def cleanlinessCheck(db):
	errBudget = 0
	errRevenue = 0
	emptyRuntime = 0
	emptyGenres = 0
	errHomepage = 0
	emptyCompnay = 0
	emptyCountry = 0
	emptySLang = 0
	emptyTitle = 0
	tooShort = 0
	totalCasts = 0
	totalCrews = 0
	for item in db:
		#We consider an attribute of some item is bad if:
		if item['budget']<0:								#the budget is a non-positive number
			errBudget += 1
		if item['genres']==[]:								#the genre information is missing
			emptyGenres += 1
		if item['homepage']!=None and item['homepage']=='':	#the homepage information is missing
			errHomepage += 1
		if item['production_companies']==[]:				#the production companies are missing
			emptyCompnay += 1
		if item['production_countries']==[]:				#the production countries are missing
			emptyCountry += 1
		if item['revenue']<0:								#the revenue is a non-positive number
			errRevenue += 1
		if item['runtime']==None:							#the runtime is missing
			emptyRuntime += 1
		elif item['runtime']<=30:							#the runtime is less than 30(minutes) for it is only a short clip and we don't consider it as a movie
			tooShort += 1
		if item['spoken_languages']==[]:					#the spoken language is missing
			emptySLang += 1
		if item['title']=='':								#the title is missing
			emptyTitle += 1
		totalCasts += len(item['cast'])
		totalCrews += len(item['crew'])
	print("errBudget = ", errBudget)
	print("errHomepage = ", errHomepage)
	print("errRevenue = ", errRevenue)
	print("emptyCountry = ", emptyCountry)
	print("emptyCompnay = ", emptyCompnay)
	print("emptyGenres = ", emptyGenres)
	print("emptyRuntime = ", emptyRuntime)
	print("emptySLang = ", emptySLang)
	print("emptyTitle = ", emptyTitle)
	print("tooShort = ", tooShort)

	#We also consider the credits information of an item is bad if:
	aveCast = totalCasts/len(db)
	aveCrew = totalCrews/len(db)
	print()
	print("aveCast = ", aveCast)
	print("aveCrew = ", aveCrew)
	fewCast = 0
	fewCrew = 0
	for item in db:
		if len(item['cast'])<aveCast/4:						#the movie has less than ave/4 cast info
			fewCast += 1
		if len(item['crew'])<aveCrew/8:						#the movie has less than ave/8 crew info
			fewCrew += 1
	print("tooFewCast = ", fewCast)
	print("fooFewCrew = ", fewCrew)

if __name__ == "__main__":
	db=load()
	cleanlinessCheck(db)
