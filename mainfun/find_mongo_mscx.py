import os 
from bs4 import BeautifulSoup as bs
import pymongo
from pymongo import MongoClient
client = MongoClient('mongodb://10.120.30.8:27017')
db = client['music']  
collect = db['mscx_c_key']
mongo_id_name=[mscx_c_key["_id"] for mscx_c_key in collect.find()]
aa=mongo_id_name[0]
for a in mongo_id_name[1:]:
	aa=aa+'|'+a
fi = open('E:/etl/find_mongo_mscx.txt','w')
fi.write(aa)
fi.close
os.system('python newcombine.py')