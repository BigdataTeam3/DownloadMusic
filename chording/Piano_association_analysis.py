# coding=utf-8

import numpy as np
from operator import itemgetter
import collections,pymongo
from pymongo import MongoClient
from decimal import Decimal, ROUND_HALF_UP
from bson.son import SON
from bson.code import Code

# 測試用

Piano_dict = {
    '0':'Piano_acoustic_grand',
    '1':'Piano_bright_acoustic',
    '2':'Piano_electric_grand',
    '3':'Piano_honky_tonk',
    '4':'Piano_electric1',
    '5':'Piano_electric2',
    '6':'Piano_harpsichord',
    '7':'Piano_clavichord',
    '8':'Piano_celesta'
}

# 轉換drum的每一個 Measure，轉成標籤 by Henry
# 第一個參數是dicts，第二個跟第三個參數是轉換標籤的比率，例0.1 or 0.2
def Association_analysis_mainfunction(dicts):

    percent_value = 0.19
    Measure_lists = Measure_extract_from_dictdata(dicts)
# print Measure_lists
    Piano_dict = Establish_piano_dict_sorted(Measure_lists)
    # print Piano_dict
    Percent_dict = Establish_percent_dict(Piano_dict)
    # print Percent_dict
    Transfer_Piano_dict = Transfer_Piano_dict_percent(Piano_dict,Percent_dict)
    # print Transfer_Piano_dict
    Measure_dict,order_value = Establish_measure_dict(Transfer_Piano_dict,percent_value)
#     print Measure_dict
#     print order_value
    Measure_dict_reverse = Transfer_dictdata(dicts,Measure_dict)
    # print Transfer_list
    Insert_piano_to_mongodb(dicts,Measure_dict_reverse)

# 先將lists of dicts 的value取出來，以一個Measure為單位，建立lists，
# 如果有多個track在同一個Measure，合併到同一個lists裡面	
def Measure_extract_from_dictdata(dicts):
    values_lists = [[value for key,value in values.items()] \
	for keyss,valuess in dicts.items() for i in valuess for keys,values in i.items()]
    values_lists = [[",".join(i)] for i in values_lists]
    return values_lists


# 累計每個Measure lists出現的次數，並建立 排序dicts，{key = measure_lists , value = 次數}，並且依次數排序
def Establish_piano_dict_sorted(values_lists):
    Piano_dict = dict()
    for measure in values_lists:
        Piano_dict[measure[0]] = Piano_dict.get(measure[0],0)+1
    Piano_dict = sorted(Piano_dict.items(), key=itemgetter(1), reverse=True)
    return Piano_dict
	
def Count_total(x, y):
    return x+y
	
def Transfer_percent(x, y):
    return round(float(x)/float(y),3)

# 從 排序dicts，再建立一個  百分比轉換dicts，{key = 次數，value = 百分比}
def Establish_percent_dict(Piano_dict):
    count_list = [i[1] for i in Piano_dict]
    count_totals = 0 
    count_totals = reduce(Count_total,count_list)
    percent_dict = {i:Transfer_percent(i,count_totals) for i in count_list}
    return percent_dict
   
# 將 排序dicts的次數，套用  百分比轉換dicts
def Transfer_Piano_dict_percent(Piano_dict,percent_dict):
    Transfer_Piano_dict = dict()
    for (key,value) in Piano_dict:
        Transfer_Piano_dict[key] = percent_dict[value]
    Transfer_Piano_dict = sorted(Transfer_Piano_dict.items(), key=itemgetter(1), reverse=True)
    return Transfer_Piano_dict

# 對轉換完的 排序dicts，根據百分比，再建立 標籤dicts，
#{Measure lists，轉成標籤，大於percent_value，為A1,A2...，小於percent_value，為B1,B2...}
def Establish_measure_dict(Transfer_Piano_dict,percent_value):
	measure_dict = dict()
	count_A = 0
	count_B = 0
	order_value = {}
	for (key,value) in Transfer_Piano_dict:
		if (value >= percent_value) and (key not in measure_dict):
			count_A += 1
			order_value.update({'A'+str(count_A):value})
			measure_dict.update({key : 'A'+str(count_A)})
		elif (percent_value > value) and (key not in measure_dict):
			count_B += 1
			order_value.update({'B'+str(count_B):value})
			measure_dict.update({key : 'B'+str(count_B)})
			
	return measure_dict,order_value

# 套用標籤dicts
# 轉換原先的dicts，全部Measure 轉成標籤
def Transfer_dictdata(dicts,measure_dict):
	Measure_dict_reverse = dict()
	values_dicts_lists = [{",".join([value for key,value in values.items()]):i \
	for keyss,valuess in dicts.items() for i in valuess for keys,values in i.items()}]
	
	Measure_dict_reverse.update({value:key for key,value in measure_dict.items()})
	Measure_dict_reverse.update({key:values for key,value in Measure_dict_reverse.items() \
	for i in values_dicts_lists for keys,values in i.items() if keys == value})
	return Measure_dict_reverse


# 塞進mongodb
def	Insert_piano_to_mongodb(dicts,Measure_dict_reverse):

	client = MongoClient('mongodb://10.120.30.8:27017')
	db = client['music']  #選擇database
	# collect = db['Piano_pattern']  #選擇database.collection
	# collect = db['Piano_pattern_with_track']  #選擇database.collection
	
	# keyword_dict = dict(keyword)
	piano_collection_number = [key[:1] for key in final_dict][0]
	
	if (str(piano_collection_number) in Piano_dict.keys()):
		piano_collection = Piano_dict[str(piano_collection_number)]
		collect = db[piano_collection]  #選擇database.collection
		
		# id_count = keyword['id_'+str(guitar_collection_number)+'_count']
		#insert_one中間的是single_staff or multi_staff
		for key,value in Measure_dict_reverse.items():
			collect.insert_one({value.keys()[0]:value.values()[0],'pattern':key[0]})
			# collect.insert_one({'_id':id_count,value.keys()[0]:value.values()[0],'pattern':key[0]})
			# id_count += 1
		
		# keyword_dict.update({"id_"+str(guitar_collection_number)+"_count":id_count})
				
		# return keyword_dict
		

#從mongodb取出
def Get_piano_from_mongodb(**keyword):
	client = MongoClient('mongodb://10.120.30.8:27017')
	db = client['music']  #選擇database
	# collect = db['Piano_pattern']  #選擇database.collection
	# collect = db['Piano_pattern_with_track']  #選擇database.collection

	get_key = keyword['get_key']
	
	if (str(get_key) in Piano_dict.keys()):
		piano_collection = Piano_dict[str(get_key)]
		collect = db[piano_collection]  #選擇database.collection
		
		cursor = collect.find({})
		piano_return_list = list()
		for doc in cursor:
			piano_return_list.append(doc)
		return piano_return_list
		
	else:
		print "請重新選擇Piano_pattern，{}".decode('cp950').format(Piano_dict.keys())

		
#piano使用，更新mongodb用，group
def piano_group_in_mongo(**keyword):

	client = MongoClient('mongodb://10.120.30.8:27017')
	db = client['music']  #選擇database
# collect = db['Piano_pattern']  #選擇database.collection
# collect = db['Piano_pattern_with_track']  #選擇database.collection
	
	get_key = keyword['get_key']
	
	if (str(get_key) in Piano_dict.keys()):
		piano_collection = Piano_dict[str(get_key)]
		collect = db[piano_collection]  #選擇database.collection
		
		#single_staff
		#使用collect.aggregate，效用等同於group，以measure的pattern搜尋，並加總、排序
		pipeline = [
					{"$group": {"_id": "$single_staff", 
					"pattern_count": {"$sum": 1}}},
					{"$sort": SON([("pattern_count", -1), ("_id", 1)])}
					]
		pattern_count_from_mongo = list(collect.aggregate(pipeline))
		
		#對group的結果，新增pattern_count field
		for pattern in pattern_count_from_mongo:
			if pattern["_id"] != None:
				collect.update_one({"single_staff":pattern["_id"]},{"$set":{"pattern_count": pattern["pattern_count"]}})
		
		#找出有single_staff field，並且沒有pattern_count field的document，並刪除
		cursor = collect.find({"single_staff":{"$exists":True},"pattern_count":{"$exists":False}})
		for doc in cursor:
		    collect.delete_one(doc)
		
		#multi_staff
		#使用collect.aggregate，效用等同於group，以measure的pattern搜尋，並加總、排序
		pipeline = [
					{"$group": {"_id": "$multi_staff", 
					"pattern_count": {"$sum": 1}}},
					{"$sort": SON([("pattern_count", -1), ("_id", 1)])}
					]
		pattern_count_from_mongo = list(collect.aggregate(pipeline))
		
		#對group的結果，新增pattern_count field
		for pattern in pattern_count_from_mongo:
			if pattern["_id"] != None:
				collect.update_one({"multi_staff":pattern["_id"]},{"$set":{"pattern_count": pattern["pattern_count"]}})
		
		#找出有multi_staff field，並且沒有pattern_count field的document，並刪除
		cursor = collect.find({"multi_staff":{"$exists":True},"pattern_count":{"$exists":False}})
		for doc in cursor:
		    collect.delete_one(doc)
		
		#刪除pattern_count這個field
		# cursor = collect.find({"single_staff":{"$exists":True},"pattern_count":{"$exists":True}}).sort("_id", pymongo.ASCENDING)
		# for doc in cursor:
			# collect.update_one({"_id":doc["_id"]},{"$unset":{"pattern_count": doc["pattern_count"]}})
			
		# cursor = collect.find({"multi_staff":{"$exists":True},"pattern_count":{"$exists":True}}).sort("_id", pymongo.ASCENDING)
		# for doc in cursor:
			# collect.update_one({"_id":doc["_id"]},{"$unset":{"pattern_count": doc["pattern_count"]}})
		
	else:
		print "請重新選擇Piano_pattern，{}".decode("cp950").format(Piano_dict.keys())
			
#piano使用，更新mongodb用，計算duration_count
def add_duration_count_in_mongo(**keyword):
	
	client = MongoClient('mongodb://10.120.30.8:27017')
	db = client['music']  #選擇database
	
	get_key = keyword['get_key']
	
	#對collect排序，把track0的measure取出，轉換每個measure，加總duration，再依排序更新collect
	if (str(get_key) in Piano_dict.keys()):
		piano_collection = Piano_dict[str(get_key)]
		collect = db[piano_collection]  #選擇database.collection
		
		cursor = collect.find({"single_staff":{"$exists":True}}).sort("_id", pymongo.ASCENDING)
		duration_count_list = [value.replace(";",",").split(",") for doc in cursor for key,value in doc["single_staff"].items() if key == "track0"]
		duration_count_list = [[Transfer_type_int_or_Decimal(j) for j in i] for i in duration_count_list]
		duration_count_list = duration_value_count(duration_count_list)
		cursor = collect.find({"single_staff":{"$exists":True}}).sort("_id", pymongo.ASCENDING)
		for i,doc in enumerate(cursor):
			collect.update_one({"_id":doc["_id"]},{"$set":{"duration_count": duration_count_list[i]}})
		
		cursor = collect.find({"multi_staff":{"$exists":True}}).sort("_id", pymongo.ASCENDING)
		duration_count_list = [value.replace(";",",").split(",") for doc in cursor for key,value in doc["multi_staff"].items() if key == "track0"]
		duration_count_list = [[Transfer_type_int_or_Decimal(j) for j in i] for i in duration_count_list]
		duration_count_list = duration_value_count(duration_count_list)
		cursor = collect.find({"multi_staff":{"$exists":True}}).sort("_id", pymongo.ASCENDING)
		for i,doc in enumerate(cursor):
			collect.update_one({"_id":doc["_id"]},{"$set":{"duration_count": duration_count_list[i]}})
			
	else:
		print "請重新選擇Piano_pattern，{}".decode("cp950").format(Piano_dict.keys())
			
#以下兩個def，搭配 add_duration_count_in_mongo 使用
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