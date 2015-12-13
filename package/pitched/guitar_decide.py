import Instrument
import random
from decimal import *
import pymongo
from pymongo import MongoClient

def patternChosen(name):
	if name.lower() == 'guitar':
		dbname = 'AG_steel'
	elif name.lower() == 'electric guitar':
		ch = {1:'EG_overdrive',2:'EG_distortion',3:'EG_muted'}
		dbname = ch[random.randint(1,3)]
	elif 'steel' in name.lower():
		dbname = 'AG_steel'
	elif 'overdrive' in name.lower():
		dbname = 'EG_overdrive'
	elif 'distortion' in name.lower():
		dbname = 'EG_distortion'
	elif 'muted' in name.lower():
		dbname = 'EG_muted'
	elif 'synth' in name.lower():
		dbname = 'EG_synth'
	elif 'nylon' in name.lower():
		dbname = 'AG_nylon'
	elif 'clean' in name.lower():
		dbname = 'EG_clean'
	elif 'harmonics' in name.lower():
		dbname = 'EG_harmonics'
	elif 'jazz' in name.lower():
		dbname = 'EG_jazz'
	else:
		dbname = None
	return dbname

def guitarChosen(name):
	if name.lower() == 'guitar':
		truename = 'Acoustic Guitar (steel)'
	elif name.lower() == 'electric guitar':
		ch = {1:'Overdriven Guitar',2:'Distortion Guitar',3:'Electric Guitar (muted)'}
		truename = ch[random.randint(1,3)]
	elif 'nylon' in name.lower():
		truename = 'Acoustic Guitar (nylon)'
	elif 'clean' in name.lower():
		truename = 'Electric Guitar (clean)'
	elif 'harmonics' in name.lower():
		truename = 'Guitar harmonics'
	else:
		truename = name
	return truename

def getGuitarPattern(dbname,notations,type,seed=None):
	if 'single' in type.lower():
		s_or_m = 'single_track'
	else:
		s_or_m = 'multi_track'
	patternDic = {}
	for notation in set(notations):
		getkey = notation[0]
		info = fromDB(dbname,getkey,s_or_m,seed=seed)
		patternDic.update({notation:info})
	return patternDic

def fromDB(dbname,get_key,s_or_m,seed=None):
	if seed:
		random.seed()
	client = MongoClient('mongodb://10.120.30.8:27017')
	db = client['music']  
	collect = db[dbname]
	
	if str(get_key) == '0':
		return {'track0':'1,0'}
	if str(get_key).lower() == 'a':
		count = collect.find({'duration_count':1,'pattern':'A',s_or_m:{'$exists':'true'}}).count()
		ran = random.randint(0,count-1)
		print ran
		cur = collect.find({'duration_count':1,'pattern':'A',s_or_m:{'$exists':'true'}})
		for i,record in enumerate(cur):
			if i == ran:
				if record.get('single_track') is not None:
					return record['single_track'] #deal with different functions
				else:
					return record['multi_track']
	
	elif str(get_key).lower() == 'b':
		count = collect.find({'duration_count':1,'pattern':'B'}).count()
		ran = random.randint(0,count-1)
		print ran
		cur = collect.find({'duration_count':1,'pattern':'B'})
		for i,record in enumerate(cur):
			if i == ran:
				if record.get('single_track') is not None:
					return record['single_track'] #deal with different functions
				else:
					return record['multi_track']
	