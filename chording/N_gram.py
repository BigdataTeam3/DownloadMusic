# coding=utf-8
# 對和弦進行排列組合
from operator import itemgetter
import csv,sys,pymongo
from math import log
from pymongo import MongoClient

chord_list = [4,8,16,32]

# def N_gram_main_function_single(chordlist):
	# N_gram_number = raw_input("請輸入N-gram-number，{}".decode('cp950').format(chord_list))
	
	# if int(N_gram_number) in chord_list:
		# chord_gram(chordlist,N_gram_number,Compare_number)

	# else :
		# print "請重新選擇chord_pattern，{}".decode('cp950').format(chord_list)
		# N_gram_main_function_single(chordlist)

def N_gram_main_function_multiple(chordlist,**keyword):
	N_gram_number = keyword['N_gram_number']
	Compare_number = keyword['Compare_number']
	
	if int(N_gram_number) in chord_list:
		chord_gram(chordlist,N_gram_number,Compare_number)
		
	else :
		print "請重新選擇chord_pattern，{}".decode('cp950').format(chord_list)

#一次抓4個
# 一次抓8個
# 一次抓16個
# 一次抓32個

def chord_gram(chordlist,N_gram_number,Compare_number):
#     print lists
	chordgram_freq = chordlist_to_chordgram(chordlist,N_gram_number)
#     print chordgram_freq
	chorddict_freq = chordgram_to_chorddict(chordgram_freq)
#     print chorddict_freq
	chordsorted_freq = sorted(chorddict_freq.items(), key=itemgetter(1), reverse=True)
#     print chordsorted_freq
#     清除可能的和弦位移
	Compare_list = chordsorted_possible_transfer_clean(chordsorted_freq)
#     這裡可以改比對的參數，以第幾個去比對
	Compare_chord,Compare_number = chordclean_to_chordcompare(Compare_list,chordsorted_freq,Compare_number)
#     開始分類
	Compare_list3 = Compare_chord_classify(Compare_chord,Compare_number,N_gram_number)
	
	Insert_chord_to_mongodb(Compare_chord,N_gram_number)
	
		
#===============================================================
#以下是共用def

# 產生N-gram
def Dominantlist_to_Dominantgram(Dominantlist,N_gram_number):
	return [Dominantlist[i:i+N_gram_number] for i in range(len(Dominantlist)-(N_gram_number-1)) if (i%2)==0]

#轉換gram to dict
def Dominantgram_to_Dominantdict(Dominantgram):
	Dominantdict = dict()
	for i in range(len(Dominantgram)):
		if Dominantgram[i][0] != 0 :
			Dominantdict[tuple(Dominantgram[i])] = Dominantdict.get(tuple(Dominantgram[i]),0)+1
	return Dominantdict


#想像[1~4]，每次往右位移2個，變成[3,4,1~2]，這些可能的變化，都不計算
#想像[1~8]，每次往右位移2個，變成[7,8,1~6]，這些可能的變化，都不計算
#想像[1~16]，每次往右位移2個，變成[15,16,1~14]，這些可能的變化，都不計算
def Dominantsorted_possible_transfer_clean(Dominantsorted):
    lists = []
    for i in range(len(Dominantsorted)):
        k = 2
        splitcount = 0
        transferlists = []
        for j in range(len(Dominantsorted[0][0])):
            if j%2==0 and j!=0 :
                splitcount += 1
                transferlists.append(Dominantsorted[i][0][(k*(splitcount)):] + Dominantsorted[i][0][:(k*(splitcount))])
        if set(transferlists).isdisjoint(set(lists)) :
            lists.append(Dominantsorted[i][0])
    return lists
#算出每種組合的出現次數,去掉重複出現的和弦組合
#找出和弦組合
def Dominantclean_to_Dominantcompare(Compare_list,Dominantsorted,Compare_number):
	Compare_Dominant = [Dominantsorted[i] for i in range(len(Dominantsorted)) for j in Compare_list if Dominantsorted[i][0] == j]
	# print "可用來比對的和弦組合".decode('cp950')
	# print Compare_Dominant
	# print "總共有幾個和弦組合可用來比對 =".decode('cp950'),len(Compare_Dominant)
	Compare_length_list = []
	Compare_length_list = [i for i in range(len(Compare_Dominant))]
	Compare_string = "請重新輸入比對的number，範圍從{}到{}".decode('cp950').format(0,Compare_length_list[-1])
	if Compare_number in Compare_length_list:
		return (Compare_Dominant,Compare_number)
	else :
		print Compare_string
		sys.exit(0)
	# Compare_number = Compare_number_func(len(Compare_Dominant))
	
	
#選擇第幾個和弦組合，可搭配N_gram_main_function_single使用
# def Compare_number_func(Compare_length):
	# Compare_length_list = []
	# Compare_length_list = [i for i in range(Compare_length)]
	# Compare_number = 0
	# Compare_number = raw_input("請輸入number，範圍從{}到{}".decode('cp950').format(Compare_length_list[0],Compare_length_list[-1]))
    # if Compare_number.isdigit():
        # if (int(Compare_number) in Compare_length_list):
            # return int(Compare_number)
        # elif (int(Compare_number) not in Compare_length_list):
            # print "請重新輸入number".decode('cp950')
            # return Compare_number_func(Compare_length)
    # else :
        # return Compare_number_func(Compare_length)

		
def Dominantsorted_count_comparator(x):
    return x[1]

#歸類的和弦，次數加總
def Dominantsorted_count_sum(x,y):
    Dominant_tuple = x[0] 
    Dominant_count_sum = x[1]+y[1]
    return (Dominant_tuple,Dominant_count_sum)
	
#目前一次四個和弦，最多錯一個和弦，然後去掉重複的，做成list，用來分類
#目前一次八個和弦，最多錯兩個和弦，然後去掉重複的，做成list，用來分類
#目前一次十六個和弦，最多錯三個和弦，然後去掉重複的，做成list，用來分類
#目前一次三十二個和弦，最多錯四個和弦，然後去掉重複的，做成list，用來分類
def Compare_Dominant_classify(Compare_Dominant,Compare_number,N_gram_number):
	Compare_list2 = []
	# print "用來比對的和弦".decode('cp950')
	# print Compare_Dominant[Compare_number][0]
	# print "和弦組合當中，類似的組合".decode('cp950')
	
	missnumber = int(log(N_gram_number,2))-1

	for i in range(len(Compare_Dominant)):
		Compare_count = 0
		for j in range(len(Compare_Dominant[0][0])):
			if cmp(Compare_Dominant[Compare_number][0][j],Compare_Dominant[i][0][j]) == 0 : Compare_count += 1       
		# print Compare_count,Compare_Dominant[i][0]
		if Compare_count >= (len(Compare_Dominant[0][0])-missnumber) : Compare_list2.append(Compare_Dominant[i])
	# print "挑選的結果".decode('cp950')
	# print Compare_list2
	# print "歸類到最多次數的和弦".decode('cp950')
	Compare_list3 = max(Compare_list2,key = Dominantsorted_count_comparator)
	Compare_list4 = reduce(Dominantsorted_count_sum,Compare_list2,[Compare_list3[0],0])
	# print Compare_list4
#     return Compare_list2,Compare_list3,Compare_list4


# 塞進mongodb
def	Insert_dominant_to_mongodb(Compare_Dominant,N_gram_number):

	client = MongoClient('mongodb://10.120.30.8:27017')
	db = client['music']  #選擇database
	
	# collect = db['dominant_gram_pattern']  #選擇database.collection
	
	# if len(Compare_Dominant) > 3:
		# for i in range(3):
			# if int(N_gram_number) in chord_list:
				# collect.replace_one({str(N_gram_number)+'_gram': Compare_Dominant[i][0]},{str(N_gram_number)+'_gram': Compare_Dominant[i][0]},upsert=True)
		
	# else:
		# for i in range(len(Compare_Dominant)):
			# if int(N_gram_number) in chord_list:
				# collect.replace_one({str(N_gram_number)+'_gram': Compare_Dominant[i][0]},{str(N_gram_number)+'_gram': Compare_Dominant[i][0]},upsert=True)
	
	
	collect = db['dominant_gram_pattern_with_no_replace']  #選擇database.collection
	
	
	#搭配 collect = db['dominant_gram_pattern_with_no_replace'] 使用
	if len(Compare_Dominant) > 3:
		for i in range(3):
			if int(N_gram_number) in chord_list:
				collect.insert_one({str(N_gram_number)+'_gram': Compare_Dominant[i][0]})
		
	else:
		for i in range(len(Compare_Dominant)):
			if int(N_gram_number) in chord_list:
				collect.insert_one({str(N_gram_number)+'_gram': Compare_Dominant[i][0]})
				
#從mongodb取出
def Get_dominant_from_mongodb(**keyword):
	client = MongoClient('mongodb://10.120.30.8:27017')
	db = client['music']  #選擇database
	collect = db['chord_gram_pattern_with_no_replace']  #選擇database.collection
	N_gram_number = keyword['N_gram_number']
	
	if int(N_gram_number) in chord_list:
		cursor = collect.find({str(N_gram_number)+'_gram':{'$exists':True}})
		Gram_list = list()
		for doc in cursor:
			Gram_list.append(doc[str(N_gram_number)+'_gram'])
		return Gram_list
		
	else:
		print "請重新選擇chord_pattern，{}".decode('cp950').format(chord_list)

		
#搭配 collect = db['chord_gram_pattern_with_no_replace'] 使用

#更新 chord mongo by group
def chord_group_in_mongo(**keyword):
	from bson.son import SON
	from bson.code import Code
	from pymongo import MongoClient

	client = MongoClient('mongodb://10.120.30.8:27017')
	db = client['music']  #選擇database
	collect = db['chord_gram_pattern_with_no_replace']  #選擇database.collection
	N_gram_number = keyword['N_gram_number']
	
	if int(N_gram_number) in chord_list:
		pipeline = [
			 {"$group": {"_id": '$'+str(N_gram_number)+'_gram', 
						 "chord_count": {"$sum": 1}}},
			{"$sort": SON([("chord_count", -1), ("_id", 1)])}
			
		]
		chord_count_from_mongo = list(collect.aggregate(pipeline))

		for chord in chord_count_from_mongo:
			if chord['_id'] != None:
		#         print chord['_id'],chord['chord_count']
				collect.update_one({str(N_gram_number)+"_gram":chord['_id']},{'$set':{"chord_count": chord["chord_count"]}})

		# cursor = collect.find({str(N_gram_number)+"_gram":{'$exists':True},'chord_count':{'$exists':True}})
		cursor = collect.find({str(N_gram_number)+"_gram":{'$exists':True},'chord_count':{'$exists':False}})

		for doc in cursor:
			collect.delete_one(doc)

	else:
		print "請重新選擇chord_pattern，{}".decode('cp950').format(chord_list)
