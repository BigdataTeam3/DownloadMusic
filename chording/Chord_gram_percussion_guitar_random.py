# coding=utf-8

#直接使用 random_main()

from pymongo import MongoClient
import pymongo,random

client = MongoClient('mongodb://10.120.30.8:27017')
db = client['music']  #選擇database

guitar_dict = {
    '24':'AG_nylon',
    '25':'AG_steel',
    '26':'EG_jazz',
    '27':'EG_clean',
    '28':'EG_muted',
    '29':'EG_overdrive',
    '30':'EG_distortion',
    '31':'EG_harmonics',
    '84':'EG_synth',
}

gram_list = [4,8,16,32]

#產出結果，gram_key字串，4g 及 8g 及 16g 及 32g 固定，後面的數字random，
#但不會超出該collection的document數量

def N_gram_random_with_N(get_gram_key):
	collect = db['clearedGramPattern']  #選擇database.collection
	N = int(get_gram_key)
	
	if N in gram_list:
		cursor = collect.find({str(N)+'gram':{'$exists':True}})
		chord_gram_count = cursor.count()
		chord_gram_random = random.randint(1,chord_gram_count)
		
		gram_string = str(N)+'g'
		gram_key = gram_string + str(chord_gram_random)
		return gram_key
	
	else:
		print "請重新選擇chord_pattern，{}".decode('cp950').format(gram_list)

# 完全random時，使用N_gram_random_without_N
# 完全random時，4g及32g，跟柏安討論後，待議

def N_gram_random_without_N():
	collect = db['clearedGramPattern']  #選擇database.collection
	
	N = random.choice(['8','16'])
	
	# gram_string = random.choice(['4g','8g','16g','32g'])
	
	cursor = collect.find({str(N)+'gram':{'$exists':True}})
	chord_gram_count = cursor.count()
	chord_gram_random = random.randint(1,chord_gram_count)
	
	gram_string = str(N)+'g'
	gram_key = gram_string + str(chord_gram_random)
	return gram_key,N

#產出結果，percussion_tuple，tuple包含字串，依據grams_key 決定tuple的長度，
# A 及 B 固定，後面的數字random，但不會超出該collection的document數量

def percussion_random_with_N(get_gram_key):
	
	N = int(get_gram_key)
	
	collect = db['percussion_pattern_with_track_A_pattern']  #選擇database.collection
	cursor = collect.find({})
	percussion_A_pattern_count = cursor.count()
	percussion_A_pattern_random = random.randint(1,percussion_A_pattern_count)

	collect = db['percussion_pattern_with_track_B_pattern']  #選擇database.collection
	cursor = collect.find({})
	percussion_B_pattern_count = cursor.count()
	percussion_B_pattern_random = random.randint(1,percussion_B_pattern_count)

	percussion_A_pattern_string = "A" + str(percussion_A_pattern_random)
	percussion_B_pattern_string = "B" + str(percussion_B_pattern_random)

	percussion_tuple = tuple([percussion_A_pattern_string]*((N/2)-1)+[percussion_B_pattern_string])
	return percussion_tuple

	
# 產出結果，collection名字 及 guitar_A_pattern_tuple
# tuple包含字串，依據grams_key 決定tuple的長度，
# A 固定，後面的數字random，但不會超出該collection的document數量

def guitar_random_with_N(get_gram_key,guitar_key):

	N = int(get_gram_key)
	guitar_key_str = str(guitar_key)
	
	guitar_string = guitar_dict[guitar_key_str]
	collect = db[guitar_string]  #選擇database.collection
	
	cursor = collect.find({'pattern':'A'}) # .sort("_id", pymongo.ASCENDING)
	guitar_A_pattern_count = cursor.count()
	guitar_A_pattern_random = random.randint(1,guitar_A_pattern_count)
	
	guitar_A_pattern_string = "A" + str(guitar_A_pattern_random)
	guitar_A_pattern_tuple = tuple([guitar_A_pattern_string]*(N/2))
	
	return guitar_string,guitar_A_pattern_tuple

# 完全random時，使用guitar_random_without_N
def guitar_random_without_N(get_gram_key):

	N = int(get_gram_key)
	
	guitar_string = random.choice([guitar_dict[key] for key in guitar_dict])
	collect = db[guitar_string]  #選擇database.collection
	
	cursor = collect.find({'pattern':'A'}) # .sort("_id", pymongo.ASCENDING)
	guitar_A_pattern_count = cursor.count()
	guitar_A_pattern_random = random.randint(1,guitar_A_pattern_count)
	
	guitar_A_pattern_string = "A" + str(guitar_A_pattern_random)
	guitar_A_pattern_tuple = tuple([guitar_A_pattern_string]*(N/2))
	
	return guitar_string,guitar_A_pattern_tuple

	
#產出結果，random_dict，{key = gram : value = {percussion_pattern + guitar_pattern}}
def random_main_with_instrument(get_gram_key,guitar_key):

	random_dict = dict()
	
	gram_key = N_gram_random_with_N(get_gram_key)
	percussion_tuple = percussion_random_with_N(get_gram_key)
	guitar_string,guitar_A_pattern_tuple = guitar_random_with_N(get_gram_key,guitar_key)
	
	random_dict.update({gram_key:{'percussion':percussion_tuple,guitar_string:guitar_A_pattern_tuple}})
	
	return random_dict

# 完全random時，使用random_main_without_instrument，可當作預設值
def random_main_without_instrument():

	random_dict = dict()
	
	gram_key,get_gram_key = N_gram_random_without_N()
	percussion_tuple = percussion_random_with_N(get_gram_key)
	guitar_string,guitar_A_pattern_tuple = guitar_random_without_N(get_gram_key)
	
	random_dict.update({gram_key:{'percussion':percussion_tuple,guitar_string:guitar_A_pattern_tuple}})
	
	return random_dict
	
	
def random_main(**keyword):

	random_list_final = list()
	
	if (len(keyword) == 3) and keyword['times'] and keyword['get_gram_key'] and keyword['guitar_key']:
		times = keyword['times'];
		get_gram_key = keyword['get_gram_key'];
		guitar_key = keyword['guitar_key'];
		if (int(get_gram_key) in gram_list) and (str(guitar_key) in guitar_dict.keys()):
			random_list_final = [[random_main_with_instrument(get_gram_key,guitar_key)]*2 for i in range(times)]
			random_list_final = [j for i in random_list_final for j in i]
			return random_list_final
		else:
			return

	elif (len(keyword) == 1) and keyword['times']:
		times = keyword['times'];
		random_list_final = [[random_main_without_instrument()]*2 for i in range(times)]
		random_list_final = [j for i in random_list_final for j in i]
		return random_list_final
		
	else:
		return
