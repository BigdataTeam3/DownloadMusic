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

#產出結果，gram_key字串，8g 及 16g 固定，後面的數字random，
#但不會超出該collection的document數量

def N_gram_random_with_N(get_key):
	collect = db['clearedGramPattern']  #選擇database.collection
	N = int(get_key)
	
	if N == 8:
		cursor = collect.find({'8gram':{'$exists':True}})
		chord_8gram_count = cursor.count()
		chord_8gram_random = random.randint(1,chord_8gram_count)
		
		gram_string = '8g'
		gram_key = gram_string + str(chord_8gram_random)
		return gram_key
		
	elif N == 16:
		cursor = collect.find({'16gram':{'$exists':True}})
		chord_16gram_count = cursor.count()
		chord_16gram_random = random.randint(1,chord_16gram_count)
		
		gram_string = '16g'
		gram_key = gram_string+str(chord_16gram_random)
		return gram_key
		
def N_gram_random_without_N():
	collect = db['clearedGramPattern']  #選擇database.collection
	
	gram_string = random.choice (['8g', '16g'])
	
	if gram_string == '8g':
		cursor = collect.find({'8gram':{'$exists':True}})
		chord_8gram_count = cursor.count()
		chord_8gram_random = random.randint(1,chord_8gram_count)
		
		gram_key = gram_string + str(chord_8gram_random)
		return gram_key
		
	elif gram_string == '16g':
		cursor = collect.find({'16gram':{'$exists':True}})
		chord_16gram_count = cursor.count()
		chord_16gram_random = random.randint(1,chord_16gram_count)
		
		gram_key = gram_string+str(chord_16gram_random)
		return gram_key
	

#產出結果，percussion_tuple，tuple包含字串，依據get_key 決定tuple的長度，
# A 及 B 固定，後面的數字random，但不會超出該collection的document數量

def percussion_random_with_N(get_key):
	
	N = int(get_key)
	
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
# tuple包含字串，依據get_key 決定tuple的長度，
# A 固定，後面的數字random，但不會超出該collection的document數量

def guitar_random_with_N(get_key):

	N = int(get_key)
	
	guitar_string = random.choice([guitar_dict[key] for key in guitar_dict])
	collect = db[guitar_string]  #選擇database.collection
	
	cursor = collect.find({'pattern':'A'}) # .sort("_id", pymongo.ASCENDING)
	guitar_A_pattern_count = cursor.count()
	guitar_A_pattern_random = random.randint(1,guitar_A_pattern_count)
	
	guitar_A_pattern_string = "A" + str(guitar_A_pattern_random)
	guitar_A_pattern_tuple = tuple([guitar_A_pattern_string]*(N/2))
	
	return guitar_string,guitar_A_pattern_tuple

	
#產出結果，random_dict，{key = gram : value = {percussion_pattern + guitar_pattern}}

def random_main(get_key):

	random_dict = dict()
	
	gram_key = N_gram_random_with_N(get_key)
	percussion_tuple = percussion_random_with_N(get_key)
	guitar_string,guitar_A_pattern_tuple = guitar_random_with_N(get_key)
	
	random_dict.update({gram_key:{'percussion':percussion_tuple,guitar_string:guitar_A_pattern_tuple}})
	
	return random_dict
	
