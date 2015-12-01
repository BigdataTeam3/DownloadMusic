from operator import itemgetter
import collections
import re

def Measure_extract_from_dictdata(test_dic):
	values_lists = [i.values() for i in test_dic.values()]
	values_lists = [[','.join(values_lists[i])] for i in range(len(values_lists))]
	values_lists = [j.replace(';',',').split(',') for i in values_lists for j in i]
	values_lists = [[Transfer_type_int_or_float(j) for j in i] for i in values_lists]
	return values_lists

def Transfer_type_int_or_float(Measure_element):
	if '.' not in Measure_element:
		return int(Measure_element)
	else:
		return float(Measure_element)
        
def Establish_percussion_dict_sorted(values_lists):
	Percussion_dict = dict()
	for measure in values_lists:
		Percussion_dict[tuple(measure)] = Percussion_dict.get(tuple(measure),0)+1
	Percussion_dict = sorted(Percussion_dict.items(), key=itemgetter(1), reverse=True)
	return Percussion_dict

def Establish_percent_dict(Percussion_dict):
	count_list = [i[1] for i in Percussion_dict]
	count_totals = 0 
	count_totals = reduce(Count_total,count_list)
	percent_dict = {i:Transfer_percent(i,count_totals) for i in count_list}
	return percent_dict
    
def Count_total(x, y):
	return x+y
    
def Transfer_percent(x, y):
	return round(float(x)/float(y),3)
    
def Transfer_percussion_dict_percent(Percussion_dict,percent_dict):
	Transfer_percussion_dict = dict()
	for (key,value) in Percussion_dict:
		Transfer_percussion_dict[key] = percent_dict[value]
	Transfer_percussion_dict = sorted(Transfer_percussion_dict.items(), key=itemgetter(1), reverse=True)
	return Transfer_percussion_dict

def Establish_measure_dict(Transfer_percussion_dict,sep_1,sep_2):
	measure_dict = dict()
	count_A = 0
	count_B = 0
	count_C = 0
	order_value = {}
	for (key,value) in Transfer_percussion_dict:
		if (value >= sep_1) and (key not in measure_dict):
			count_A += 1
			order_value.update({'A'+str(count_A):value})
			measure_dict.update({key : 'A'+str(count_A)})
		elif value >= sep_2:
			count_B += 1
			order_value.update({'B'+str(count_B):value})
			measure_dict.update({key : 'B'+str(count_B)})
		else:
			count_C += 1
			order_value.update({'C'+str(count_C):value})
			measure_dict.update({key : 'C'+str(count_C)})
	return (measure_dict,order_value)

def Transfer_dictdata(test_dic,measure_dict):
	for keys,values in test_dic.items():
		for key,value in values.items():
			value = ','.join(values.values())
			value = value.replace(';',',').split(',')
			value = tuple(Transfer_type_int_or_float(i) for i in value)
			test_dic.update({keys : measure_dict[value]})
	return test_dic




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
