import pymongo
from pymongo import MongoClient
import re
import random


def getGrams(grampatterns):
	client = MongoClient('mongodb://10.120.30.8:27017')
	db = client['music']
	collect = db['gramPattern']
	dic = dict()
	for u in set(grampatterns):
		if u == '0':
			continue
		p = re.match('(\d+)',u).group(1)
		if int(p)%4 != 0:
			print 'No such patterns..'
			return None
		count = collect.find({p+'gram':{'$exists':'true'}},{'_id':0}).count()
		ran = random.randint(0,count)
		cur = collect.find({p+'gram':{'$exists':'true'}},{'_id':0}).sort('total',pymongo.DESCENDING)
		for n,record in enumerate(cur):
			if n == ran:
				dic.update({u:record[p+'gram']})
				break
				
	return_chords = []
	for pattern in grampatterns:
		if pattern == '0':
			return_chords.append('0')
		else:
			[return_chords.append(str(pa)) for pa in dic[pattern]]
			
	return return_chords