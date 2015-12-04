# coding=utf-8

import numpy as np
from operator import itemgetter
import collections,pymongo
from pymongo import MongoClient
import re

# 轉換drum的每一個 Measure，轉成標籤 by Henry
# 第一個參數是dicts，第二個跟第三個參數是轉換標籤的比率，例0.1 or 0.2
# 找出打擊樂(鼓)常見的形式
# measure(小節)
# track(聲部) track0:打A樂器;track1:打B樂器;track2:打C樂器;出現在同一小節時,各自打擊自己的節奏
# 以下dic是字典，沒有排序
def Association_analysis_mainfunction(dicts,percent_value_ceiling=0.21,percent_value_floor=0.08):
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
	Transfer_dic = Transfer_dictdata(dicts,Measure_dict)
	# print Transfer_dic
	Insert_percussion_to_mongodb(Transfer_percussion_dict,percent_value_ceiling,percent_value_floor)
	

#每個小節所有track合併
# def Measure_extract_from_dictdata(dicts):
    # values_lists = [i.values() for i in dicts.values()]
    # values_lists = [[','.join(values_lists[i])] for i in range(len(values_lists))]
    # values_lists = [j.replace(';',',').split(',') for i in values_lists for j in i]
    # values_lists = [[Transfer_type_int_or_float(j) for j in i] for i in values_lists]
    # return values_lists

	
# 先將dicts of dicts 的value取出來，以一個Measure為單位，建立lists，
# 如果有多個track在同一個Measure，合併到同一個lists裡面	
def Measure_extract_from_dictdata(dicts):
	values_lists = [i.values() for i in dicts.values()]
	values_lists = [[i[j]] for i in values_lists for j in range(len(i))]	
	return values_lists

#搭配合併track的list
# def Transfer_type_int_or_float(Measure_element):
    # if '.' not in Measure_element:
        # return int(Measure_element)
    # else:
        # return float(Measure_element)

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
		if (value >= percent_value_ceiling) and ([key][0] not in measure_dict):
			count_A += 1
			order_value.update({'A'+str(count_A):value})
			measure_dict.update({[key][0] : 'A'+str(count_A)})
		elif (percent_value_ceiling > value >= percent_value_floor) and ([key][0] not in measure_dict):
			count_B += 1
			order_value.update({'B'+str(count_B):value})
			measure_dict.update({[key][0] : 'B'+str(count_B)})
		else:
			count_C += 1
			order_value.update({'C'+str(count_C):value})
			measure_dict.update({[key][0] : 'C'+str(count_C)})
	return measure_dict,order_value

# 套用標籤dicts
# 轉換原先的dicts，全部Measure 轉成標籤
def Transfer_dictdata(dicts,measure_dict):
    for keys,values in dicts.items():
        for key,value in values.items():
            values.update({keys : measure_dict[value]})
    return dicts




# 塞進mongodb
def	Insert_percussion_to_mongodb(Transfer_percussion_dict,percent_value_ceiling,percent_value_floor):

	client = MongoClient('mongodb://10.120.30.8:27017')
	db = client['music']  #選擇database
	collect = db['percussion_pattern']  #選擇database.collection
	
	for i in Transfer_percussion_dict:
		if i[1] >= percent_value_ceiling:
			collect.replace_one({'A_pattern': i[0]},{'A_pattern': i[0]},upsert=True)
	
		elif percent_value_ceiling > i[1] >= percent_value_floor:
			collect.replace_one({'B_pattern': i[0]},{'B_pattern': i[0]},upsert=True)
		
		else :
			collect.replace_one({'C_pattern': i[0]},{'C_pattern': i[0]},upsert=True)

#從mongodb取出
def Get_percussion_from_mongodb(get_key):
	client = MongoClient('mongodb://10.120.30.8:27017')
	db = client['music']  #選擇database
	collect = db['percussion_pattern']  #選擇database.collection
	
	if (str(get_key) == 'A') or (str(get_key) == 'a'):
		cursor = collect.find({'A_pattern':{'$exists':True}})
		A_pattern_list = list()
		for doc in cursor:
			A_pattern_list.append(doc['A_pattern'])
		return A_pattern_list
	
	elif (str(get_key) == 'B') or (str(get_key) == 'b'):
		cursor = collect.find({'B_pattern':{'$exists':True}})
		B_pattern_list = list()
		for doc in cursor:
			B_pattern_list.append(doc['B_pattern'])
		return B_pattern_list
	
	elif (str(get_key) == 'C') or (str(get_key) == 'c'):
		cursor = collect.find({'C_pattern':{'$exists':True}})
		C_pattern_list = list()
		for doc in cursor:
			C_pattern_list.append(doc['C_pattern'])
		return C_pattern_list
	
	else:
		print "請重新選擇percussion_pattern，A or B or C".decode('cp950')
		
def asso_main(staff,sep_1,sep_2):
	dict2 = staff.copy()
	Measure_lists = Measure_extract_from_dictdata(dict2)
	Percussion_dict = Establish_percussion_dict_sorted(Measure_lists)
	Percent_dict = Establish_percent_dict(Percussion_dict)
	Transfer_percussion_dict = Transfer_percussion_dict_percent(Percussion_dict,Percent_dict)
	Measure_dict = Establish_measure_dict(Transfer_percussion_dict,sep_1,sep_2)
	Transfer_dic = Transfer_dictdata(dict2,Measure_dict[0])
	measure_dic = {}
	for measure in Transfer_dic:
		measure_dic.update({int(re.match('.*?(\d+)',measure).group(1)):Transfer_dic[measure]})
	pattern = [measure_dic[a] for a in sorted(measure_dic)]
	return (pattern,Measure_dict[1])
