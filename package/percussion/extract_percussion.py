import numpy as np
from decimal import *

time = {
	'measure':Decimal(1),
	'whole':Decimal(1),
	'half':Decimal(1)/2,
	'quarter':Decimal(1)/4,
	'eighth':Decimal(1)/8,
	'16th':Decimal(1)/16,
	'32nd':Decimal(1)/32,
	'64th':Decimal(1)/64,
	'128th':Decimal(1)/128
}

def ifDots(tag):
	if not tag.find('dots'):
		multi = 1
	else:
		dots = tag.find('dots').text
		if dots == '1':
			multi = 1.5
		elif dots == '2':
			multi = 1.75
		elif dots == '3':
			multi = 1.875
	return Decimal(multi)

def get_perc_pattern(staff,division,sigN,sigD):
	time = {
	'measure':None,
	'whole':Decimal(1),
	'half':Decimal(1)/2,
	'quarter':Decimal(1)/4,
	'eighth':Decimal(1)/8,
	'16th':Decimal(1)/16,
	'32nd':Decimal(1)/32,
	'64th':Decimal(1)/64,
	'128th':Decimal(1)/128
	}
	time['measure'] = sigN/sigD
	time_acc = 0
	tupletID = ''
	tupletRatio = 1
	dic = {}
	for num,measure in enumerate(staff.select('Measure')):
		measure_key = 'measure_' + measure.get('number')
		check_tick = num*division*4
		dic.update({measure_key:{}}) 
		for tag in measure.find_all(['Rest','Chord','Tuplet','TimeSig','tick']):
			if tag.name == 'tick':
				if tag.text == str(check_tick):
					continue
				else:
					print 'error : ticking at the wrong time', 'skip measure '+ measure.get('number')
					break
            
			if tag.name == 'Chord' or tag.name == 'Rest':
				multi = ifDots(tag)
				duTime = Decimal(time[tag.select('durationType')[0].text])
				time_acc = duTime * multi
			if not tag.find('track'):
				track_key = 'track' + '0'
			else:
				track_key = 'track' + tag.find('track').text

			if dic[measure_key].get(track_key) is None:
				dic[measure_key].update({track_key:''})
			if tag.name == 'Rest':
				if dic[measure_key][track_key] == '':
					dic[measure_key][track_key] += str(time_acc) + ',0'
				else:
					dic[measure_key][track_key] += ';' + str(time_acc) + ',0'
			elif tag.name == 'Chord':
				pitches = tag.select('pitch')
				addlist = [time_acc] + [int(a.text) for a in pitches]
				if dic[measure_key][track_key] == '':
					dic[measure_key][track_key] += ','.join([str(c) for c in addlist])
				else:
					dic[measure_key][track_key] += ';' + ','.join([str(c) for c in addlist])
			elif tag.name == 'Tuplet' and tag.get('id'):
				tupletID = tag['id']
				normalNotes = Decimal(tag.find('normalNotes').text)
				actualNotes = Decimal(tag.find('actualNotes').text)
				tupletRatio = normalNotes / actualNotes

			elif tag.name == 'TimeSig':
				sigN = Decimal(tag.find('sigN').text)
				sigD = Decimal(tag.find('sigD').text)
				if sigN/sigD != time['measure']:
					time['measure'] = sigN/sigD
	return dic

def return_pattern(music):
	m = music.select('Part > Staff')
	division = int(music.find('Division').text)
	staff1TimeSig = music.select_one('Score > Staff:nth-of-type(1) TimeSig')
	sigN = Decimal(staff1TimeSig.find('sigN').text)
	sigD = Decimal(staff1TimeSig.find('sigD').text)
	percussions = [s.get('id') for s in filter(lambda x: len(x.select('defaultClef'))>0 and x.defaultClef.text == 'PERC', music.select('Part > Staff'))]
	per_staffs = filter(lambda x: x.get('id') in percussions,music.select('Score > Staff'))
	perdic = {}
	for staff in per_staffs:
		perdic.update({'staff_'+staff.get('id'):get_perc_pattern(staff,division,sigN,sigD)})
	return perdic