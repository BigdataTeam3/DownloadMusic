import combining_tracks
import Determine_Chord_final
from bs4 import BeautifulSoup as bs
import sys
from decimal import *

def paraHandler(commands):
	d = {}
	for p in commands:
		if p.startswith('-'):
			para_num = p.split('-')[1]
			continue
		else:
			if para_num == 'm':
				d['main_melody'] = p.strip().split(',')
			if para_num == 'r':
				d['user_removed'] = p.strip().split(',')
	return d
	
def findChords(addr,main_melody=None):
	if type(main_melody) == type(u''):
		melodies = main_melody.encode('utf8').strip().split(',')
	elif type(main_melody) == type(''):
		melodies = main_melody.strip().split(',')
	elif main_melody is not None:
		melodies = [str(a) for a in list(main_melody)]
	f = open(addr,'r')
	music = bs(f.read(),'xml')
	f.close()
	staff1TimeSig = music.select_one('Score > Staff:nth-of-type(1) TimeSig')
	division = int(music.find('Division').text)
	sigN = Decimal(staff1TimeSig.find('sigN').text)
	sigD = Decimal(staff1TimeSig.find('sigD').text)
	staffs_dic = {}
	nonpitched = map(lambda x: x.get('id') if x.StaffType.get('group') != 'pitched' else 0,music.select('Part > Staff'))
	pitched_staffs = filter(lambda x: x.get('id') not in nonpitched,music.select('Score > Staff'))
	if main_melody is not None:
		OK_staffs = filter(lambda x: x.get('id') not in melodies,pitched_staffs)
	else:
		OK_staffs = pitched_staffs
	for staff in OK_staffs:
		staffs_dic.update({'staff_'+staff.get('id') : combining_tracks.one_track_chord(staff,division,sigN,sigD)})
	result_chords = combining_tracks.combining_chords(staffs_dic,division,sigN,sigD)
	
	combined_chords = Determine_Chord_final.comb_chords(result_chords)
	final_chords = Determine_Chord_final.final_determined(combined_chords)
	return final_chords
