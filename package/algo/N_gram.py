# coding=big5
from operator import itemgetter
import csv
from math import log

def N_gram_main_function(Dominantlist,N_gram_number):
	if N_gram_number == 4:
		Dominantlist_4_gram_number(Dominantlist,N_gram_number)
	elif N_gram_number == 8:
		Dominantlist_8_gram_number(Dominantlist,N_gram_number)
	elif N_gram_number == 16:
		Dominantlist_16_gram_number(Dominantlist,N_gram_number)
	else :
		print u'請重新輸入N-gram-number，4 or 8 or 16'


#一次抓4個
	
def Dominantlist_4_gram_number(Dominantlist,N_gram_number):
#     print Dominantlist
	Dominantgram_4freq = Dominantlist_to_Dominantgram(Dominantlist,N_gram_number)
#     print Dominantgram_4freq
	Dominantdict_4freq = Dominantgram_to_Dominantdict(Dominantgram_4freq)
#     print Dominantdict_4freq
	Dominantsorted_4freq = sorted(Dominantdict_4freq.items(), key=itemgetter(1), reverse=True)
#     print Dominantsorted_4freq
#     清除可能的和弦位移
	Compare_list = Dominantsorted_possible_transfer_clean(Dominantsorted_4freq)
#     這裡可以改比對的參數，以第幾個去比對
	Compare_Dominant,Compare_number = Dominantclean_to_Dominantcompare(Compare_list,Dominantsorted_4freq)
#     開始分類
	Compare_list3 = Compare_Dominant_classify(Compare_Dominant,Compare_number,N_gram_number)

	

#一次抓8個

def Dominantlist_8_gram_number(Dominantlist,N_gram_number):
#     print Dominantlist
	Dominantgram_8freq = Dominantlist_to_Dominantgram(Dominantlist,N_gram_number)
#     print Dominantgram_8freq
	Dominantdict_8freq = Dominantgram_to_Dominantdict(Dominantgram_8freq)
#     print Dominantdict_8freq
	Dominantsorted_8freq = sorted(Dominantdict_8freq.items(), key=itemgetter(1), reverse=True)
#     print Dominantsorted_8freq
#     清除可能的和弦位移
	Compare_list = Dominantsorted_possible_transfer_clean(Dominantsorted_8freq)
#     這裡可以改比對的參數，以第幾個去比對
	Compare_Dominant,Compare_number = Dominantclean_to_Dominantcompare(Compare_list,Dominantsorted_8freq)
#     開始分類
	Compare_list3 = Compare_Dominant_classify(Compare_Dominant,Compare_number,N_gram_number)


#一次抓16個

def Dominantlist_16_gram_number(Dominantlist,N_gram_number):
#     print Dominantlist
	Dominantgram_16freq = Dominantlist_to_Dominantgram(Dominantlist,N_gram_number)
#     print Dominantgram_16freq
	Dominantdict_16freq = Dominantgram_to_Dominantdict(Dominantgram_16freq)
#     print Dominantdict_16freq
	Dominantsorted_16freq = sorted(Dominantdict_16freq.items(), key=itemgetter(1), reverse=True)
#     print Dominantsorted_16freq
#     清除可能的和弦位移
	Compare_list = Dominantsorted_possible_transfer_clean(Dominantsorted_16freq)
#     這裡可以改比對的參數，以第幾個去比對
	Compare_Dominant,Compare_number = Dominantclean_to_Dominantcompare(Compare_list,Dominantsorted_16freq)
#     開始分類
	Compare_list3 = Compare_Dominant_classify(Compare_Dominant,Compare_number,N_gram_number)
	
	
#===============================================================
#以下是共用def

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

#找出和弦組合
def Dominantclean_to_Dominantcompare(Compare_list,Dominantsorted):
	Compare_Dominant = [Dominantsorted[i] for i in range(len(Dominantsorted)) for j in Compare_list if Dominantsorted[i][0] == j]
	print u'可用來比對的和弦組合'
	print Compare_Dominant
	print u'總共有幾個和弦組合可用來比對 =',len(Compare_list)
	Compare_number = Compare_number_func(len(Compare_list))
	return Compare_Dominant,Compare_number
	
#選擇第幾個和弦組合
def Compare_number_func(Compare_length):
    Compare_length_list = []
    Compare_length_list = [i for i in range(Compare_length)]
    Compare_number = 0
    Compare_number = raw_input(u"請輸入number，範圍從{}到{}".format(Compare_length_list[0],Compare_length_list[-1]))
    if Compare_number.isdigit():
        if (int(Compare_number) in Compare_length_list):
            return int(Compare_number)
        elif (int(Compare_number) not in Compare_length_list):
            print u'請重新輸入number'
            return Compare_number_func(Compare_length)
    else :
        return Compare_number_func(Compare_length)

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
def Compare_Dominant_classify(Compare_Dominant,Compare_number,N_gram_number):
	Compare_list2 = []
	print u'用來比對的和弦'
	print Compare_Dominant[Compare_number][0]
	print u'和弦組合當中，類似的組合'
	
	missnumber = int(log(N_gram_number,2))-1

	for i in range(len(Compare_Dominant)):
		Compare_count = 0
		for j in range(len(Compare_Dominant[0][0])):
			if cmp(Compare_Dominant[Compare_number][0][j],Compare_Dominant[i][0][j]) == 0 : Compare_count += 1       
		print Compare_count,Compare_Dominant[i][0]
		if Compare_count >= (len(Compare_Dominant[0][0])-missnumber) : Compare_list2.append(Compare_Dominant[i])
	print u'挑選的結果'
	print Compare_list2
	print u'歸類到最多次數的和弦'
	Compare_list3 = max(Compare_list2,key = Dominantsorted_count_comparator)
	Compare_list4 = reduce(Dominantsorted_count_sum,Compare_list2,[Compare_list3[0],0])
	print Compare_list4
#     return Compare_list2,Compare_list3
