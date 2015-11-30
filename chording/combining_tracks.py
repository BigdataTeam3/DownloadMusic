from decimal import *
import re

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
	
def one_track_chord(staff,division,sigN,sigD):
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
	track_0_time_acc = 0
	tupletID = ''
	tupletRatio = 1
	thistrack = {}
	ticking = None
	for tag in staff.find_all(['Rest','Chord','Tuplet','TimeSig','tick']):
		if tag.name == 'tick':
			ticking = int(tag.text)
			time_acc = 0
		if tag.name == 'Chord' or tag.name == 'Rest': 
			if not tag.find('track'):
				istrack = False
				track_key = 'track' + '0'
				if thistrack.get(track_key) is None:
					thistrack.update({track_key:[]})
			else:
				istrack = True
				track_key = 'track' + tag.find('track').text
				if thistrack.get(track_key) is None:
					thistrack.update({track_key:[]})
			multi = ifDots(tag)
			if tag.find('Tuplet') and tag.find('Tuplet').text == tupletID:
				multi *= tupletRatio
			duTime = Decimal(time[tag.select('durationType')[0].text])
			time_acc += duTime * multi
			if istrack == False:
				track_0_time_acc += duTime * multi
			if tag.name == 'Rest':
				if ticking:
					thistrack[track_key].append(ticking)
					ticking = None
				if istrack == True:
					thistrack[track_key].append((time_acc, 0))
				else:
					thistrack[track_key].append((track_0_time_acc, 0))
			else:
				pitches = tag.select('pitch')
				if ticking:
					thistrack[track_key].append(ticking)
					ticking = None
				if istrack == True:
					addlist = [time_acc] + [int(a.text) for a in pitches]
					thistrack[track_key].append(tuple(addlist))
				else:
					addlist = [track_0_time_acc] + [int(a.text) for a in pitches]
					thistrack[track_key].append(tuple(addlist))
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
	return thistrack

def adjust_tracks(staff,division,sigN):
	ret_dic = {}
	ticks_per_measure = int(sigN)*int(division)
	ret_dic.update({'track0':filter(lambda g: type(g) != type(1),staff['track0'])})
	for track in [t for t in staff if t != 'track0']:
		adding = []
		for info in staff[track]:
			if type(info) == type(1):
				now_beats = Decimal(info)/ticks_per_measure
				adding.append((now_beats,0))
			else:
				if info[1] == 0:
					adding.append((info[0]+now_beats,0))
				else:
					ll = [info[0]+now_beats] + list(info[1:])
					adding.append(tuple(ll))
		ret_dic.update({track:adding})
		adding = []
	return ret_dic
	
def add_tracks(added_staff):
	chord_dic = {}
	for track in added_staff:
		chord_gogo = {}
		count = 0
		begin = 0
		while(count < added_staff[track][-1][0]):
			while(count < added_staff[track][begin][0]):
				if added_staff[track][begin][1] == 0:
					chord_gogo.update({count:[]})
				else:
					now =added_staff[track][begin][1:]
					chord_gogo.update({count:now})
				count += 1.0/8
			begin += 1
		chord_dic.update({track : chord_gogo})
	return chord_dic
	
def combining_chords(staffs_dic,division,sigN,sigD):
	combined_staffs = {}
	for staff in staffs_dic:
		seted_staff = add_tracks(adjust_tracks(staffs_dic[staff],division,sigN))
		combined_staffs.update({staff:{}})
		for track in seted_staff:
			for timestamp in seted_staff[track]:
				if combined_staffs[staff].get(timestamp) is None:
					combined_staffs[staff].update({timestamp:set(seted_staff[track][timestamp])})
				else:
					combined_staffs[staff][timestamp] = combined_staffs[staff][timestamp]|set(seted_staff[track][timestamp])
	return combined_staffs