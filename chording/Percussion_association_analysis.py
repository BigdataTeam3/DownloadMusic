# coding=utf-8

import numpy as np
from operator import itemgetter
import collections,pymongo
from pymongo import MongoClient

# 轉換drum的每一個 Measure，轉成標籤 by Henry
# 第一個參數是dicts，第二個跟第三個參數是轉換標籤的比率，例0.1 or 0.2
# 找出打擊樂(鼓)常見的形式
# measure(小節)
# track(聲部) track0:打A樂器;track1:打B樂器;track2:打C樂器;出現在同一小節時,各自打擊自己的節奏
# 以下dic是字典，沒有排序

pattern_list = ['A','a','B','b','C','c']

def Association_analysis_mainfunction(dicts,**keyword):
	percent_value_ceiling = 0.21;
	percent_value_floor = 0.08;
	Measure_lists = Measure_extract_from_dictdata(dicts)
# print Measure_lists
	Percussion_dict = Establish_percussion_dict_sorted(Measure_lists)
# print Percussion_dict
	Percent_dict = Establish_percent_dict(Percussion_dict)
# print Percent_dict
	Transfer_percussion_dict = Transfer_percussion_dict_percent(Percussion_dict,Percent_dict)
# print Transfer_percussion_dict
	Measure_dict,order_value = Establish_measure_dict(Transfer_percussion_dict,percent_value_ceiling,percent_value_floor)
# print Measure_dict
	Transfer_dic,Measure_dict_reverse = Transfer_dictdata(dicts,Measure_dict)
	# print Transfer_dic
	keyword_dict = Insert_percussion_to_mongodb(Transfer_dic,Measure_dict_reverse,**keyword)
	
	return keyword_dict
	


# 先將dicts of dicts 的value取出來，以一個Measure為單位，建立lists，
# 如果有多個track在同一個Measure，合併到同一個lists裡面	
def Measure_extract_from_dictdata(dicts):
	values_lists = [i for i in dicts.values()]
	values_lists = [[i[j] for j in i] for i in values_lists ]
	values_lists = [[",".join(i)] for i in values_lists ]
	return values_lists


# 累計每個Measure lists出現的次數，並建立 排序dicts，{key = measure_lists , value = 次數}，並且依次數排序
def Establish_percussion_dict_sorted(values_lists):
    Percussion_dict = dict()
    for measure in values_lists:
        Percussion_dict[measure[0]] = Percussion_dict.get(measure[0],0)+1
    Percussion_dict = sorted(Percussion_dict.items(), key=itemgetter(1), reverse=True)
    return Percussion_dict
	
def Count_total(x, y):
    return x+y
	
def Transfer_percent(x, y):
    return round(float(x)/float(y),3)

# 從 排序dicts，再建立一個  百分比轉換dicts，{key = 次數，value = 百分比}
def Establish_percent_dict(Percussion_dict):
    count_list = [i[1] for i in Percussion_dict]
    count_totals = 0 
    count_totals = reduce(Count_total,count_list)
    percent_dict = {i:Transfer_percent(i,count_totals) for i in count_list}
    return percent_dict
   
# 將 排序dicts的次數，套用  百分比轉換dicts
def Transfer_percussion_dict_percent(Percussion_dict,percent_dict):
    Transfer_percussion_dict = dict()
    for (key,value) in Percussion_dict:
        Transfer_percussion_dict[key] = percent_dict[value]
    Transfer_percussion_dict = sorted(Transfer_percussion_dict.items(), key=itemgetter(1), reverse=True)
    return Transfer_percussion_dict

# 對轉換完的 排序dicts，根據百分比，再建立 標籤dicts，
#{Measure lists，轉成標籤，大於percent_value，為A1,A2...，小於percent_value，為B1,B2...}
def Establish_measure_dict(Transfer_percussion_dict,percent_value_ceiling,percent_value_floor):
	measure_dict = dict()
	count_A = 0
	count_B = 0
	count_C = 0
	order_value = {}
	for (key,value) in Transfer_percussion_dict:
		if (value >= percent_value_ceiling) and (key not in measure_dict):
			count_A += 1
			order_value.update({'A'+str(count_A):value})
			measure_dict.update({key : 'A'+str(count_A)})
		elif (percent_value_ceiling > value >= percent_value_floor) and (key not in measure_dict):
			count_B += 1
			order_value.update({'B'+str(count_B):value})
			measure_dict.update({key : 'B'+str(count_B)})
		else:
			count_C += 1
			order_value.update({'C'+str(count_C):value})
			measure_dict.update({key : 'C'+str(count_C)})
	return measure_dict,order_value

# 套用標籤dicts
# 轉換原先的dicts，全部Measure 轉成標籤
def Transfer_dictdata(dicts,measure_dict):
    Measure_dict_reverse = dict()
    for keys,values in dicts.items():
        for key,value in values.items():
            value = ','.join(values.values())
            Measure_dict_reverse.update({v:values for k,v in measure_dict.items() if value == k})
            dicts.update({keys : measure_dict[value]})
    Measure_dict_reverse = sorted(Measure_dict_reverse.items(),key=itemgetter(0))
    return dicts,Measure_dict_reverse




# 塞進mongodb
def	Insert_percussion_to_mongodb(Transfer_dic,Measure_dict_reverse,**keyword):

	client = MongoClient('mongodb://10.120.30.8:27017')
	db = client['music']  #選擇database
	# collect = db['percussion_pattern']  #選擇database.collection
	# collect = db['percussion_pattern_with_track']  #選擇database.collection
	
	keyword_dict = dict(keyword)
	
	for keys in Measure_dict_reverse:
	
		pattern_string = keys[0][0]
		id_count = keyword['id_'+str(pattern_string)+'_count']
		
		percussion_collection = "percussion_pattern_with_track_" + str(pattern_string) + "_pattern"
		collect = db[percussion_collection]  #選擇database.collection
			
		collect.insert_one({'_id':id_count,str(pattern_string)+'_pattern':keys[1]})
		# collect.replace_one({{'_id':id_count},{str(pattern_string)+'_pattern':keys[1]}},{{'_id':id_count},{str(pattern_string)+'_pattern':keys[1]}},upsert=True)
		id_count += 1
		
		keyword_dict.update({"id_"+str(pattern_string)+"_count":id_count})
			
	return keyword_dict

#從mongodb取出
def Get_percussion_from_mongodb(**keyword):
	client = MongoClient('mongodb://10.120.30.8:27017')
	db = client['music']  #選擇database
	# collect = db['percussion_pattern']  #選擇database.collection
	# collect = db['percussion_pattern_with_track']  #選擇database.collection
	
	get_key = keyword['get_key']
	
	if str(get_key) in pattern_list:
	
		percussion_collection = "percussion_pattern_with_track_" + str(get_key) + "_pattern"
		collect = db[percussion_collection]  #選擇database.collection
		
		cursor = collect.find({str(get_key)+'_pattern':{'$exists':True}})
		percussion_pattern_return_list = list()
		for doc in cursor:
			percussion_pattern_return_list.append(doc[str(get_key)+'_pattern'])
		return percussion_pattern_return_list
	
	else:
		print "請重新選擇percussion_pattern，{}".decode('cp950').format(pattern_list)


		
#percussion使用，更新mongodb用，group
def percussion_group_in_mongo(**keyword):
	from pymongo import MongoClient
	import pymongo
	client = MongoClient('mongodb://10.120.30.8:27017')
	db = client['music']  #選擇database
# collect = db['percussion_pattern']  #選擇database.collection
# collect = db['percussion_pattern_with_track']  #選擇database.collection
	
	get_key = keyword['get_key']
	
	if str(get_key) in pattern_list:
	
		percussion_collection = "percussion_pattern_with_track_" + str(get_key) + "_pattern"
		collect = db[percussion_collection]  #選擇database.collection
		
		#使用collect.aggregate，效用等同於group，以measure的pattern搜尋，並加總、排序
		pipeline = [
					{"$group": {"_id": '$'+str(get_key)+'_pattern', 
					"pattern_count": {"$sum": 1}}},
					{"$sort": SON([("pattern_count", -1), ("_id", 1)])}
					]
		pattern_count_from_mongo = list(collect.aggregate(pipeline))
		
		#對group的結果，新增pattern_count field
		for pattern in pattern_count_from_mongo:
			# print pattern['_id'],pattern['pattern_count']
			if pattern["_id"] != None:
				collect.update_one({str(get_key)+"_pattern":pattern['_id']},{'$set':{"pattern_count": pattern['pattern_count']}})
		
		#找出有A_pattern field，並且沒有pattern_count field的document，並刪除
		# cursor = collect.find({str(get_key)+'_pattern':{'$exists':True},'pattern_count':{'$exists':True}})
		cursor = collect.find({str(get_key)+'_pattern':{'$exists':True},'pattern_count':{'$exists':False}})
		for doc in cursor:
		    collect.delete_one(doc)
		
		#對剩下的doc，比對_id field，如果_id 不等於 i+1，則新增doc，刪除舊的doc
		for i,doc in enumerate(collect.find({}).sort('_id', pymongo.ASCENDING)):
			# print i+1,doc['_id'],doc[str(get_key)+'_pattern'],doc['pattern_count']
			if (i+1) != doc['_id']:
				newdoc = {"_id":i+1,str(get_key)+"_pattern":doc[str(get_key)+'_pattern']}
				collect.insert_one(newdoc)
				collect.delete_one({'_id':doc['_id']})
		
		#刪除pattern_count這個field
		for i,doc in enumerate(collect.find({}).sort('_id', pymongo.ASCENDING)):
			collect.update_one({'_id':doc['_id']},{'$unset':{"pattern_count": doc['pattern_count']}})
			
	else:
		print "請重新選擇percussion_pattern，{}".decode('cp950').format(pattern_list)

			
#percussion使用，更新mongodb用，計算duration_count
def add_duration_count_in_mongo(**keyword):
	
	client = MongoClient('mongodb://10.120.30.8:27017')
	db = client['music']  #選擇database
	
	get_key = keyword['get_key']
	
	#對collect排序，把track0的measure取出，轉換每個measure，加總duration，再依排序更新collect
	if str(get_key) in pattern_list:
	
		percussion_collection = "percussion_pattern_with_track_" + str(get_key) + "_pattern"
		collect = db[percussion_collection]  #選擇database.collection
		
		cursor = collect.find({}).sort('_id', pymongo.ASCENDING)
		duration_count_list = [value.replace(';',',').split(',') for docs in cursor for key,value in docs[str(get_key)+'_pattern'].items() if key == 'track0']
		duration_count_list = [[Transfer_type_int_or_float(j) for j in i] for i in duration_count_list]
		duration_count_list = duration_value_count(duration_count_list)
		
		for i,doc in enumerate(collect.find({}).sort('_id', pymongo.ASCENDING)):
#     print i,doc['_id'],doc,duration_count_list[i]
			collect.update_one({'_id':doc['_id']},{'$set':{"duration_count": duration_count_list[i]}})
	
	else:
		print "請重新選擇percussion_pattern，{}".decode('cp950').format(pattern_list)
			
#以下兩個def，搭配 add_duration_count_in_mongo 使用
def Transfer_type_int_or_float(Measure_element):
    if '.' not in Measure_element:
        return int(Measure_element)
    else:
        return float(Measure_element)   

def duration_value_count(lists):
    count_list =list()
    for i in lists:
        count_totals = 0
        if i[0] == 1:
            count_list.append(1.0)
        else:
            for j in i:
                if type(j) == float:
                    count_totals += j
            count_list.append(count_totals)        
    return count_list
