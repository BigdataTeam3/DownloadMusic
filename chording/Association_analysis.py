# coding=utf-8

import numpy as np
from operator import itemgetter
import collections,pymongo
from pymongo import MongoClient

# �ഫdrum���C�@�� Measure�A�ন���� by Henry
# �Ĥ@�ӰѼƬOdicts�A�ĤG�Ӹ�ĤT�ӰѼƬO�ഫ���Ҫ���v�A��0.1 or 0.2
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
	

#�C�Ӥp�`�Ҧ�track�X��
# def Measure_extract_from_dictdata(dicts):
    # values_lists = [i.values() for i in dicts.values()]
    # values_lists = [[','.join(values_lists[i])] for i in range(len(values_lists))]
    # values_lists = [j.replace(';',',').split(',') for i in values_lists for j in i]
    # values_lists = [[Transfer_type_int_or_float(j) for j in i] for i in values_lists]
    # return values_lists

	
# ���Ndicts of dicts ��value���X�ӡA�H�@��Measure�����A�إ�lists�A
# �p�G���h��track�b�P�@��Measure�A�X�֨�P�@��lists�̭�	
def Measure_extract_from_dictdata(dicts):
	values_lists = [i.values() for i in dicts.values()]
	values_lists = [[i[j]] for i in values_lists for j in range(len(i))]	
	return values_lists

#�f�t�X��track��list
# def Transfer_type_int_or_float(Measure_element):
    # if '.' not in Measure_element:
        # return int(Measure_element)
    # else:
        # return float(Measure_element)

# �֭p�C��Measure lists�X�{�����ơA�ëإ� �Ƨ�dicts�A{key = measure_lists , value = ����}�A�åB�̦��ƱƧ�
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

# �q �Ƨ�dicts�A�A�إߤ@��  �ʤ����ഫdicts�A{key = ���ơAvalue = �ʤ���}
def Establish_percent_dict(Percussion_dict):
    count_list = [i[1] for i in Percussion_dict]
    count_totals = 0 
    count_totals = reduce(Count_total,count_list)
    percent_dict = {i:Transfer_percent(i,count_totals) for i in count_list}
    return percent_dict
   
# �N �Ƨ�dicts�����ơA�M��  �ʤ����ഫdicts
def Transfer_percussion_dict_percent(Percussion_dict,percent_dict):
    Transfer_percussion_dict = dict()
    for (key,value) in Percussion_dict:
        Transfer_percussion_dict[key] = percent_dict[value]
    Transfer_percussion_dict = sorted(Transfer_percussion_dict.items(), key=itemgetter(1), reverse=True)
    return Transfer_percussion_dict

# ���ഫ���� �Ƨ�dicts�A�ھڦʤ���A�A�إ� ����dicts�A
#{Measure lists�A�ন���ҡA�j��percent_value�A��A1,A2...�A�p��percent_value�A��B1,B2...}
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

# �M�μ���dicts
# �ഫ�����dicts�A����Measure �ন����
def Transfer_dictdata(dicts,measure_dict):
    for keys,values in dicts.items():
        for key,value in values.items():
            values.update({keys : measure_dict[value]})
    return dicts




# ��imongodb
def	Insert_percussion_to_mongodb(Transfer_percussion_dict,percent_value_ceiling,percent_value_floor):

	client = MongoClient('mongodb://10.120.30.8:27017')
	db = client['music']  #���database
	collect = db['percussion_pattern']  #���database.collection
	
	for i in Transfer_percussion_dict:
		if i[1] >= percent_value_ceiling:
			collect.replace_one({'A_pattern': i[0]},{'A_pattern': i[0]},upsert=True)
	
		elif percent_value_ceiling > i[1] >= percent_value_floor:
			collect.replace_one({'B_pattern': i[0]},{'B_pattern': i[0]},upsert=True)
		
		else :
			collect.replace_one({'C_pattern': i[0]},{'C_pattern': i[0]},upsert=True)

#�qmongodb���X
def Get_percussion_from_mongodb(get_key):
	client = MongoClient('mongodb://10.120.30.8:27017')
	db = client['music']  #���database
	collect = db['percussion_pattern']  #���database.collection
	
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
		print "�Э��s���percussion_pattern�AA or B or C".decode('cp950')