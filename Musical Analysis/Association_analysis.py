# coding=utf-8

import numpy as np
from operator import itemgetter
import collections

# �ഫdrum���C�@�� Measure�A�ন���� by Henry
# �Ĥ@�ӰѼƬOdicts�A�ĤG�ӰѼƬO�ഫ���Ҫ���v�A��0.1 or 0.2
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

# ���Ndicts of dicts ��value���X�ӡA�H�@��Measure�����A�إ�lists�A
# �p�G���h��track�b�P�@��Measure�A�X�֨�P�@��lists�̭�
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

# �֭p�C��Measure lists�X�{�����ơA�ëإ� �Ƨ�dicts�A{key = measure_lists , value = ����}�A�åB�̦��ƱƧ�
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

# �q �Ƨ�dicts�A�A�إߤ@��  �ʤ����ഫdicts�A{key = ���ơAvalue = �ন�ʤ���}
def Establish_percent_dict(Percussion_dict):
    count_list = [i[1] for i in Percussion_dict]
    count_totals = 0 
    count_totals = reduce(Count_total,count_list)
    percent_dict = {i:Transfer_percent(i,count_totals) for i in count_list}
    return percent_dict
   
# �N �Ƨ�dicts�A�M��  �ʤ����ഫdicts
def Transfer_percussion_dict_percent(Percussion_dict,percent_dict):
    Transfer_percussion_dict = dict()
    for (key,value) in Percussion_dict:
        Transfer_percussion_dict[key] = percent_dict[value]
    Transfer_percussion_dict = sorted(Transfer_percussion_dict.items(), key=itemgetter(1), reverse=True)
    return Transfer_percussion_dict

# ���ഫ���� �Ƨ�dicts�A�ھڦʤ���A�A�إ� ����dicts�A
#{Measure lists�A�ন���ҡA�j��percent_value�A��A1,A2...�A�p��percent_value�A��B1,B2...}
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

# �M�μ���dicts
# �ഫ�����dicts�A����Measure �ন����
def Transfer_dictdata(dicts,measure_dict):
    for keys,values in dicts.items():
        for key,value in values.items():
            value = ','.join(values.values())
            value = value.replace(';',',').split(',')
            value = tuple(Transfer_type_int_or_float(i) for i in value)
            dicts.update({keys : measure_dict[value]})
    return dicts
    


#  �t�~���ƧǡA�w�� Measure_dict�A�i��|�Ψ�
# measure_dict_sort = [[Measure,len(Measure),Measure_dict[Measure]] for Measure in \
#                      sorted(Measure_dict, key=lambda Measure: len(Measure), reverse=True)]
# print measure_dict_sort
# Transfer_dic = sorted(Transfer_dic.items(), key = itemgetter(0))


