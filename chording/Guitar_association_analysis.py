# coding=utf-8

import numpy as np
from operator import itemgetter
import collections,pymongo
from pymongo import MongoClient
from decimal import Decimal, ROUND_HALF_UP
from bson.son import SON
from bson.code import Code

# ���ե�
# guitar_dict = {
    # '24':'AG_nylon',
    # '25':'AG_steel',
    # '26':'EG_jazz',
    # '27':'EG_clean',
    # '28':'EG_muted',
    # '29':'EG_overdrive',
    # '30':'EG_distortion',
    # '31':'EG_harmonics',
    # '84':'EG_synth',
# }

guitar_dict = {
    '24':'Acoustic_guitar_nylon',
    '25':'Acoustic_guitar_steel',
    '26':'Electric_guitar_jazz',
    '27':'Electric_guitar_clean',
    '28':'Electric_guitar_muted',
    '29':'Electric_guitar_overdrive',
    '30':'Electric_guitar_distortion',
    '31':'Electric_Guitar_harmonics',
    '84':'Electric_guitar_synth',
}



# �ഫdrum���C�@�� Measure�A�ন���� by Henry
# �Ĥ@�ӰѼƬOdicts�A�ĤG�Ӹ�ĤT�ӰѼƬO�ഫ���Ҫ���v�A��0.1 or 0.2
def Association_analysis_mainfunction(dicts,**keyword):

    percent_value = 0.19
    Measure_lists = Measure_extract_from_dictdata(dicts)
# print Measure_lists
    Guitar_dict = Establish_guitar_dict_sorted(Measure_lists)
    # print Guitar_dict
    Percent_dict = Establish_percent_dict(Guitar_dict)
    # print Percent_dict
    Transfer_guitar_dict = Transfer_guitar_dict_percent(Guitar_dict,Percent_dict)
    # print Transfer_guitar_dict
    Measure_dict,order_value = Establish_measure_dict(Transfer_guitar_dict,percent_value)
#     print Measure_dict
#     print order_value
    Measure_dict_reverse = Transfer_dictdata(dicts,Measure_dict)
	# print Transfer_list
    keyword_dict = Insert_guitar_to_mongodb(dicts,Measure_dict_reverse,**keyword)
	
    return keyword_dict

	
# ���Nlists of dicts ��value���X�ӡA�H�@��Measure�����A�إ�lists�A
# �p�G���h��track�b�P�@��Measure�A�X�֨�P�@��lists�̭�	
def Measure_extract_from_dictdata(dicts):
    values_lists = [[value for key,value in values.items()] \
	for keyss,valuess in dicts.items() for i in valuess for keys,values in i.items()]
    values_lists = [[",".join(i)] for i in values_lists]
    return values_lists


# �֭p�C��Measure lists�X�{�����ơA�ëإ� �Ƨ�dicts�A{key = measure_lists , value = ����}�A�åB�̦��ƱƧ�
def Establish_guitar_dict_sorted(values_lists):
    Guitar_dict = dict()
    for measure in values_lists:
        Guitar_dict[measure[0]] = Guitar_dict.get(measure[0],0)+1
    Guitar_dict = sorted(Guitar_dict.items(), key=itemgetter(1), reverse=True)
    return Guitar_dict
	
def Count_total(x, y):
    return x+y
	
def Transfer_percent(x, y):
    return round(float(x)/float(y),3)

# �q �Ƨ�dicts�A�A�إߤ@��  �ʤ����ഫdicts�A{key = ���ơAvalue = �ʤ���}
def Establish_percent_dict(Guitar_dict):
    count_list = [i[1] for i in Guitar_dict]
    count_totals = 0 
    count_totals = reduce(Count_total,count_list)
    percent_dict = {i:Transfer_percent(i,count_totals) for i in count_list}
    return percent_dict
   
# �N �Ƨ�dicts�����ơA�M��  �ʤ����ഫdicts
def Transfer_guitar_dict_percent(Guitar_dict,percent_dict):
    Transfer_guitar_dict = dict()
    for (key,value) in Guitar_dict:
        Transfer_guitar_dict[key] = percent_dict[value]
    Transfer_guitar_dict = sorted(Transfer_guitar_dict.items(), key=itemgetter(1), reverse=True)
    return Transfer_guitar_dict

# ���ഫ���� �Ƨ�dicts�A�ھڦʤ���A�A�إ� ����dicts�A
#{Measure lists�A�ন���ҡA�j��percent_value�A��A1,A2...�A�p��percent_value�A��B1,B2...}
def Establish_measure_dict(Transfer_guitar_dict,percent_value):
	measure_dict = dict()
	count_A = 0
	count_B = 0
	order_value = {}
	for (key,value) in Transfer_guitar_dict:
		if (value >= percent_value) and (key not in measure_dict):
			count_A += 1
			order_value.update({'A'+str(count_A):value})
			measure_dict.update({key : 'A'+str(count_A)})
		elif (percent_value > value) and (key not in measure_dict):
			count_B += 1
			order_value.update({'B'+str(count_B):value})
			measure_dict.update({key : 'B'+str(count_B)})
			
	return measure_dict,order_value

# �M�μ���dicts
# �ഫ�����dicts�A����Measure �ন����
def Transfer_dictdata(dicts,measure_dict):
	Measure_dict_reverse = dict()
	values_dicts_lists = [{",".join([value for key,value in values.items()]):i \
	for keyss,valuess in dicts.items() for i in valuess for keys,values in i.items()}]
	
	Measure_dict_reverse.update({value:key for key,value in measure_dict.items()})
	Measure_dict_reverse.update({key:values for key,value in Measure_dict_reverse.items() \
	for i in values_dicts_lists for keys,values in i.items() if keys == value})
	return Measure_dict_reverse


# ��imongodb
def	Insert_guitar_to_mongodb(dicts,Measure_dict_reverse,**keyword):

	client = MongoClient('mongodb://10.120.30.8:27017')
	db = client['music']  #���database
	# collect = db['guitar_pattern']  #���database.collection
	# collect = db['guitar_pattern_with_track']  #���database.collection
	
	keyword_dict = dict(keyword)
	guitar_collection_number = [key[:2] for key in dicts][0]
	
	if (str(guitar_collection_number) in guitar_dict.keys()):
		guitar_collection = guitar_dict[str(guitar_collection_number)]
		collect = db[guitar_collection]  #���database.collection
		
		id_count = keyword['id_'+str(guitar_collection_number)+'_count']
		#insert_one�������Osingle_track or multi_track
		for key,value in Measure_dict_reverse.items():
			collect.insert_one({'_id':id_count,value.keys()[0]:value.values()[0],'pattern':key[0]})
			id_count += 1
		
		keyword_dict.update({"id_"+str(guitar_collection_number)+"_count":id_count})
				
		return keyword_dict


#�qmongodb���X
def Get_guitar_from_mongodb(**keyword):
	client = MongoClient('mongodb://10.120.30.8:27017')
	db = client['music']  #���database
	# collect = db['guitar_pattern']  #���database.collection
	# collect = db['guitar_pattern_with_track']  #���database.collection

	get_key = keyword['get_key']
	
	if (str(get_key) in guitar_dict.keys()):
		guitar_collection = guitar_dict[str(get_key)]
		collect = db[guitar_collection]  #���database.collection
		
		cursor = collect.find({})
		guitar_return_list = list()
		for doc in cursor:
			guitar_return_list.append(doc)
		return guitar_return_list
		
	else:
		print "�Э��s���guitar_pattern�A{}".decode('cp950').format(guitar_dict.keys())

		
#guitar�ϥΡA��smongodb�ΡAgroup
def guitar_group_in_mongo(**keyword):

	client = MongoClient('mongodb://10.120.30.8:27017')
	db = client['music']  #���database
# collect = db['guitar_pattern']  #���database.collection
# collect = db['guitar_pattern_with_track']  #���database.collection
	
	get_key = keyword['get_key']
	
	if (str(get_key) in guitar_dict.keys()):
		guitar_collection = guitar_dict[str(get_key)]
		collect = db[guitar_collection]  #���database.collection
		
		#single_track
		#�ϥ�collect.aggregate�A�ĥε��P��group�A�Hmeasure��pattern�j�M�A�å[�`�B�Ƨ�
		pipeline = [
					{"$group": {"_id": "$single_track", 
					"pattern_count": {"$sum": 1}}},
					{"$sort": SON([("pattern_count", -1), ("_id", 1)])}
					]
		pattern_count_from_mongo = list(collect.aggregate(pipeline))
		
		#��group�����G�A�s�Wpattern_count field
		for pattern in pattern_count_from_mongo:
			if pattern["_id"] != None:
				collect.update_one({"single_track":pattern["_id"]},{"$set":{"pattern_count": pattern["pattern_count"]}})
		
		#��X��single_track field�A�åB�S��pattern_count field��document�A�çR��
		cursor = collect.find({"single_track":{"$exists":True},"pattern_count":{"$exists":False}})
		for doc in cursor:
		    collect.delete_one(doc)
		
		#multi_track
		#�ϥ�collect.aggregate�A�ĥε��P��group�A�Hmeasure��pattern�j�M�A�å[�`�B�Ƨ�
		pipeline = [
					{"$group": {"_id": "$multi_track", 
					"pattern_count": {"$sum": 1}}},
					{"$sort": SON([("pattern_count", -1), ("_id", 1)])}
					]
		pattern_count_from_mongo = list(collect.aggregate(pipeline))
		
		#��group�����G�A�s�Wpattern_count field
		for pattern in pattern_count_from_mongo:
			if pattern["_id"] != None:
				collect.update_one({"multi_track":pattern["_id"]},{"$set":{"pattern_count": pattern["pattern_count"]}})
		
		#��X��multi_track field�A�åB�S��pattern_count field��document�A�çR��
		cursor = collect.find({"multi_track":{"$exists":True},"pattern_count":{"$exists":False}})
		for doc in cursor:
		    collect.delete_one(doc)
		
		#��ѤU��doc�A���_id field�A�p�G_id ������ i+1�A�h�s�Wdoc�A�R���ª�doc
		cursor = collect.find({}).sort("_id", pymongo.ASCENDING)
		for i,doc in enumerate(cursor):
			if doc.keys()[2] == "single_track":
				newdoc = {"_id":str(i+1)+"_single","single_track":doc["single_track"],"pattern":doc["pattern"]}
				collect.insert_one(newdoc)
				collect.delete_one({"_id":doc["_id"]})
			elif doc.keys()[2] == "multi_track":
				newdoc = {"_id":str(i+1)+"_multi","multi_track":doc["multi_track"],"pattern":doc["pattern"]}
				collect.insert_one(newdoc)
				collect.delete_one({"_id":doc["_id"]})
		
		id_count = 1
		cursor = collect.find({"single_track":{"$exists":True}}).sort("_id", pymongo.ASCENDING)
		for doc in cursor:
			newdoc = {"_id":id_count,"single_track":doc["single_track"],"pattern":doc["pattern"]}
			collect.insert_one(newdoc)
			collect.delete_one({"_id":doc["_id"]})
			id_count += 1
		
		cursor = collect.find({"multi_track":{"$exists":True}}).sort("_id", pymongo.ASCENDING)
		for doc in cursor:
			newdoc = {"_id":id_count,"multi_track":doc["multi_track"],"pattern":doc["pattern"]}
			collect.insert_one(newdoc)
			collect.delete_one({"_id":doc["_id"]})
			id_count += 1
		
		#�R��pattern_count�o��field
		# cursor = collect.find({"single_track":{"$exists":True},"pattern_count":{"$exists":True}}).sort("_id", pymongo.ASCENDING)
		# for doc in cursor:
			# collect.update_one({"_id":doc["_id"]},{"$unset":{"pattern_count": doc["pattern_count"]}})
			
		# cursor = collect.find({"multi_track":{"$exists":True},"pattern_count":{"$exists":True}}).sort("_id", pymongo.ASCENDING)
		# for doc in cursor:
			# collect.update_one({"_id":doc["_id"]},{"$unset":{"pattern_count": doc["pattern_count"]}})
		
	else:
		print "�Э��s���guitar_pattern�A{}".decode("cp950").format(guitar_dict.keys())
			
#guitar�ϥΡA��smongodb�ΡA�p��duration_count
def add_duration_count_in_mongo(**keyword):
	
	client = MongoClient('mongodb://10.120.30.8:27017')
	db = client['music']  #���database
	
	get_key = keyword['get_key']
	
	#��collect�ƧǡA��track0��measure���X�A�ഫ�C��measure�A�[�`duration�A�A�̱Ƨǧ�scollect
	if (str(get_key) in guitar_dict.keys()):
		guitar_collection = guitar_dict[str(get_key)]
		collect = db[guitar_collection]  #���database.collection
		
		cursor = collect.find({"single_track":{"$exists":True}}).sort("_id", pymongo.ASCENDING)
		duration_count_list = [doc['single_track'].values()[0].replace(";",",").split(",") for doc in cursor]
		duration_count_list = [[Transfer_type_int_or_Decimal(j) for j in i] for i in duration_count_list]
		duration_count_list = duration_value_count(duration_count_list)
		cursor = collect.find({"single_track":{"$exists":True}}).sort("_id", pymongo.ASCENDING)
		for i,doc in enumerate(cursor):
			collect.update_one({"_id":doc["_id"]},{"$set":{"duration_count": duration_count_list[i]}})
		
		cursor = collect.find({"multi_track":{"$exists":True}}).sort("_id", pymongo.ASCENDING)
		duration_count_list = [doc['multi_track'].values()[0].replace(";",",").split(",") for doc in cursor]
		duration_count_list = [[Transfer_type_int_or_Decimal(j) for j in i] for i in duration_count_list]
		duration_count_list = duration_value_count(duration_count_list)
		cursor = collect.find({"multi_track":{"$exists":True}}).sort("_id", pymongo.ASCENDING)
		for i,doc in enumerate(cursor):
			collect.update_one({"_id":doc["_id"]},{"$set":{"duration_count": duration_count_list[i]}})
			
	else:
		print "�Э��s���guitar_pattern�A{}".decode("cp950").format(guitar_dict.keys())
			
#�H�U���def�A�f�t add_duration_count_in_mongo �ϥ�
def Transfer_type_int_or_Decimal(Measure_element):
    if "." in Measure_element:
        return Decimal(Measure_element)
    else:
        return int(Measure_element)  

def duration_value_count(lists):
    count_list = list()
    for i in lists:
        count_totals = 0
        if i[0] == 1:
            count_list.append(1.0)
        else:
            for j in i:
                if type(j) == Decimal:
                    count_totals += j
            count_list.append(float(Decimal(count_totals).quantize(Decimal("1.0000"), rounding=ROUND_HALF_UP)))

    return count_list