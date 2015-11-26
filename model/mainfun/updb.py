import sys
import pyodbc
import os
import time
try:
	for line in sys.stdin:
		print line.strip()
	filename=line.strip().split(',')[0]
	tonality=line.strip().split(',')[1]
	staff_id=line.strip().split(',')[2]
	if len(line.strip().split(','))>3:
		for b in line.strip().split(',')[3:]:
			staff_id=staff_id+','+b
	addr = 'E:/musicteam/newmusic'
	targetname = addr+'/'+filename.encode('utf8')
	fj = open(targetname,'r')
	fjcontent = fj.read()
	fj.close()
	import pymongo
	from pymongo import MongoClient
	client = MongoClient('mongodb://10.120.30.8:27017')
	db = client['music']  
	collect = db['mscx_c_key']
	dic = {'_id':filename,'data':fjcontent,'tonality':tonality,'main_melody':staff_id}
	collect.insert_one(dic) 
#	collect.update({'_id':filename},dic)
#	print filename+',updateOK!!!!!!!!'
except:
	print filename+',error'


