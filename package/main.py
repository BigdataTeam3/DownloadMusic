import musicMaker
def makeSheet(ins_list):
	ins_list = list(eval(ins_list))
	mc = musicMaker.MusicCreator()
	mc.determineChords(['8g1','8g1','8g1','8g1','8g2','8g2','8g2','8g2'])
	#mc.setChords(['Am','F','C','G','Am','F','C','G','Am','F','C','G','Am','F','C','G'\
	#			 ,'Am','F','C','G','Am','F','C','G','Am','F','C','G','Am','F','C','G'\
	#			 ,'Am','F','C','G','Am','F','C','G','Am','F','C','G','Am','F','C','G'\
	#			 ,'Am','F','C','G','Am','F','C','G','Am','F','C','G','Am','F','C','G'])
	if 'percussion' in ins_list:
		per_notation = ['0','0','0','0','0','0','0','0',\
					 'A2','A2','A2','B2','A2','A2','A2','B2',\
					 '0','0','0','0','0','0','0','0',\
					 'A2','A2','A2','B2','A2','A2','A2','B2']
		per1 = mc.getMeasuresPerByNotations(per_notation)
		mc.addStaff(per1,'percussionType')
		with open('C:/Users/BigData/Desktop/abcd.txt','a') as f:
			f.write('\n percussion')
	
	if 'percussion_solo' in ins_list:
		solo_notation = ['0','0','0','0','0','0','0','0',\
				'0','0','0','0','0','0','0','0',\
				'A1','A1','A1','A1','C1','C2','C3','C4',\
				'0','0','0','0','0','0','0','0']
		persolo = mc.getMeasuresPerByNotations(solo_notation)
		mc.addStaff(persolo,'percussionType',solo=True)
		mc.addLongStaffByChords('Synth Voice',match=solo_notation)
		with open('C:/Users/BigData/Desktop/abcd.txt','a') as f:
			f.write('\n percussion_solo')
		
	if 'guitar' in ins_list:
		guitar_chord = ['0','0','0','0','0','0','0','0',\
				'A7','A7','A7','A7','A7','A7','A7','A7',\
				'0','0','0','0','0','0','0','0',\
				'A7','A7','A7','A7','A7','A7','A7','A7']
		mgui1 = mc.getGuitarPitByNotations(guitar_chord,'single')
		mc.addStaff(mgui1,instrument='Electric Guitar (jazz)')
		with open('C:/Users/BigData/Desktop/abcd.txt','a') as f:
			f.write('\n guitar')
		
	if 'electric_guitar' in ins_list:
		guitar_split = ['A7','A7','A7','A7','A7','A7','A7','A7',\
				'A8','A8','A8','A8','A8','A8','A8','A8',\
				'0','0','0','0','0','0','0','0',\
				'0','0','0','0','0','0','0','0']
		mgui2 = mc.getGuitarPitByNotations(guitar_split,'multi')
		mc.addStaff(mgui2,instrument='Acoustic Guitar (steel)')
		with open('C:/Users/BigData/Desktop/abcd.txt','a') as f:
			f.write('\n electric_guitar')

	sheet = mc.createSheet()
	with open('C:/Users/BigData/Desktop/mscx/music.mscx','w') as f:
		f.write(str(sheet))