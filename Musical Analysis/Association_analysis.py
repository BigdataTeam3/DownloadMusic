# coding=utf-8

import numpy as np
from operator import itemgetter
import collections

# 轉換drum的每一個 Measure，轉成標籤 by Henry
# 第一個參數是dicts，第二個參數是轉換標籤的比率，例0.1 or 0.2
def Association_analysis_mainfunction(dicts,percent_value):
	Measure_lists = Measure_extract_from_dictdata(dicts)
# print Measure_lists
	Percussion_dict = Establish_percussion_dict_sorted(Measure_lists)
# print Percussion_dict
	Percent_dict = Establish_percent_dict(Percussion_dict)
# print Percent_dict
	Transfer_percussion_dict = Transfer_percussion_dict_percent(Percussion_dict,Percent_dict)
# print Transfer_percussion_dict
	Measure_dict = Establish_measure_dict(Transfer_percussion_dict,percent_value)
# print Measure_dict
	Transfer_dic = Transfer_dictdata(dicts,Measure_dict)
	print Transfer_dic

# 先將dicts of dicts 的value取出來，以一個Measure為單位，建立lists，
# 如果有多個track在同一個Measure，合併到同一個lists裡面
def Measure_extract_from_dictdata(dicts):
    values_lists = [i.values() for i in dicts.values()]
    values_lists = [[','.join(values_lists[i])] for i in range(len(values_lists))]
    values_lists = [j.replace(';',',').split(',') for i in values_lists for j in i]
    values_lists = [[Transfer_type_int_or_float(j) for j in i] for i in values_lists]
    return values_lists

def Transfer_type_int_or_float(Measure_element):
    if '.' not in Measure_element:
        return int(Measure_element)
    else:
        return float(Measure_element)

# 累計每個Measure lists出現的次數，並建立 排序dicts，{key = measure_lists , value = 次數}，並且依次數排序
def Establish_percussion_dict_sorted(values_lists):
    Percussion_dict = dict()
    for measure in values_lists:
        Percussion_dict[tuple(measure)] = Percussion_dict.get(tuple(measure),0)+1
    Percussion_dict = sorted(Percussion_dict.items(), key=itemgetter(1), reverse=True)
    return Percussion_dict

def Count_total(x, y):
    return x+y
	
def Transfer_percent(x, y):
    return round(float(x)/float(y),3)

# 從 排序dicts，再建立一個  百分比轉換dicts，{key = 次數，value = 轉成百分比}
def Establish_percent_dict(Percussion_dict):
    count_list = [i[1] for i in Percussion_dict]
    count_totals = 0 
    count_totals = reduce(Count_total,count_list)
    percent_dict = {i:Transfer_percent(i,count_totals) for i in count_list}
    return percent_dict
   
# 將 排序dicts，套用  百分比轉換dicts
def Transfer_percussion_dict_percent(Percussion_dict,percent_dict):
    Transfer_percussion_dict = dict()
    for (key,value) in Percussion_dict:
        Transfer_percussion_dict[key] = percent_dict[value]
    Transfer_percussion_dict = sorted(Transfer_percussion_dict.items(), key=itemgetter(1), reverse=True)
    return Transfer_percussion_dict

# 對轉換完的 排序dicts，根據百分比，再建立 標籤dicts，
#{Measure lists，轉成標籤，大於percent_value，為A1,A2...，小於percent_value，為B1,B2...}
def Establish_measure_dict(Transfer_percussion_dict,percent_value):
    measure_dict = dict()
    count_A = 0
    count_B = 0
    for (key,value) in Transfer_percussion_dict:
        if (value >= percent_value) and (key not in measure_dict):
            count_A += 1
            measure_dict.update({key : 'A'+str(count_A)})
        else :
            count_B += 1
            measure_dict.update({key : 'B'+str(count_B)})
    return measure_dict

# 套用標籤dicts
# 轉換原先的dicts，全部Measure 轉成標籤
def Transfer_dictdata(dicts,measure_dict):
    for keys,values in dicts.items():
        for key,value in values.items():
            value = ','.join(values.values())
            value = value.replace(';',',').split(',')
            value = tuple(Transfer_type_int_or_float(i) for i in value)
            dicts.update({keys : measure_dict[value]})
    return dicts
    


#  另外的排序，針對 Measure_dict，可能會用到
# measure_dict_sort = [[Measure,len(Measure),Measure_dict[Measure]] for Measure in \
#                      sorted(Measure_dict, key=lambda Measure: len(Measure), reverse=True)]
# print measure_dict_sort
# Transfer_dic = sorted(Transfer_dic.items(), key = itemgetter(0))


