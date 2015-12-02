import os 
from bs4 import BeautifulSoup as bs
main_name = ['melody','melodie','vocal','voice','sing','lead']
sub_name = ['drum']
mongo_id_name=[]
fi = open('E:/etl/find_mongo_mscx.txt','r')
mongo_id_name=fi.read().split('|')
fi.close
newmusic_filename=[filename for filename in os.listdir('E:/musicteam/newmusic')]
for filename in list(set(newmusic_filename)-set(mongo_id_name)):

#for filename in os.listdir('E:/musicteam/newmusic'):
	fm = open('E:/musicteam/newmusic/'+filename,'r')
	music = fm.read()
	fm.close()
	cand = bs(music,'xml').select('Part')
	main_cand = []
	main_cand_staff=[]
	ismaster = {}
	for s in [par for par in cand if len(par.select('longName')) != 0]:
		pname = s.select('longName')[0].text.encode('utf8').lower()
		for staff in s.select('Staff'):
			i = staff.get('id') 
			value=0
			if len([word for word in main_name if word in pname]) != 0: # instru. name
				main_cand.append(s)
				main_cand_staff.append(i)
				value=1
			ismaster.update({i:value})
	if sum(ismaster.values())>0:
		fi = open('E:/etl/mainfun/MyData.csv','w')
		fi.write('staff,mainMelody')
		fi.write('\n')
		for i in main_cand_staff:
			fi.write(str(i)+',1')
			fi.write('\n')
		fi.close()
		os.system('echo '+filename+' | python key.py | python updb.py') 
	else:
		os.system('echo '+filename+' | python ex2.py')
		os.system('Rscript Rmainfunc.R')
		os.system('echo '+filename+' | python key.py | python updb.py') 


 