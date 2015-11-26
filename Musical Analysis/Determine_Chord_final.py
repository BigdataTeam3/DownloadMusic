import numpy as np
from decimal import *
import sys
import math
from bs4 import BeautifulSoup as bs

def convert(tu):
    origin = [0,0,0,0,0,0,0,0,0,0,0,0]
    for i in tu:
        origin[i%12]=1
    return tuple(origin)
chord = {
    convert((0,4,7)):'C',convert((2,5,9)):'Dm',convert((4,7,11)):'Em',
    convert((0,5,9)):'F',convert((2,7,11)):'G',convert((0,4,9)):'Am',
    convert((2,5,10)):'Bb',convert((2,5,11)):'Bdim'
}
chord_np = np.array(chord.keys())

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


def nearest(nparray, pt):
    n = [math.sqrt(sum((i-pt)**2)) for i in nparray]
    mindis = min(n)
    idx = n.index(mindis)
    return nparray[idx]

ar = sys.argv


base_addr = '\\'.join(ar[0].split('\\')[:-1])+'\\'
musicname = ar[1]
f = open(base_addr+musicname,'r')
music = bs(f.read(),'xml')
f.close()
staff1TimeSig = music.select_one('Score > Staff:nth-of-type(1) TimeSig')
sigN = Decimal(staff1TimeSig.find('sigN').text)
sigD = Decimal(staff1TimeSig.find('sigD').text)
time['measure'] = sigN/sigD
l = []
dic = {}
nonpitched = set(map(lambda x: x.get('id') if x.StaffType.get('group') != 'pitched' else 0,music.select('Part > Staff')))
for staff in set(music.select('Score > Staff'))-nonpitched:
    time_acc = 0
    tupletID = ''
    tupletRatio = 1
    for tag in staff.find_all(['Rest','Chord','Tuplet','TimeSig']):
        if (tag.name == 'Chord' or tag.name == 'Rest') and not tag.find('track'):
            multi = ifDots(tag)
            if tag.find('Tuplet') and tag.find('Tuplet').text == tupletID:
                multi *= tupletRatio
            duTime = Decimal(time[tag.select('durationType')[0].text])
            time_acc += duTime * multi
            if tag.name == 'Rest':
                l.append((time_acc, 0))
            else:
                pitches = tag.select('pitch')             
                addlist = [time_acc] + [int(a.text) for a in pitches]
                l.append(tuple(addlist))
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
    dic.update({'staff_'+staff.get('id') : l})
    l = []
	
pitch_count = 0
percent = 0.5
def have_chord(li):
    return float(len([a for a in li if len(a)>2]))
def have_note(li):
    return float(len([a for a in li if a[1] != 0]))
dominant_percent_staff_list = filter(lambda x: have_chord(dic[x])/have_note(dic[x]) >= percent,dic)

shifting_staff_list = []
det_mult = 2
for staff in dominant_percent_staff_list:
    chord_count = 0
    chord_half_count = 0
    chord_one_count = 0
    count = 0
    begin = 0        
    while(count < dic[staff][-1][0]):
        while(count < dic[staff][begin][0]):
            if dic[staff][begin][1] != 0:
                if count*8 % 4 == 0:
                    chord_count += 1
                elif count*8 % 4 == 1:
                    chord_half_count += 1
                elif count*8 % 4 == 2:
                    chord_one_count += 1 
            count += 1.0/8
        begin += 1
    if chord_count==0:   
        if chord_one_count>=chord_half_count:
            shifting_staff_list.append((staff,1.0/4))
        elif chord_half_count>chord_one_count:
            shifting_staff_list.append((staff,1.0/8))
    else:
        if float(chord_one_count)/chord_count>det_mult:
            shifting_staff_list.append((staff,1.0/4))
        elif float(chord_half_count)/chord_count>det_mult:
            shifting_staff_list.append((staff,1.0/8))
        else:
            shifting_staff_list.append((staff,0))
		
chord_dic = {}
for staff,shift in shifting_staff_list:
    chord_gogo = []
    count = shift
    begin = 0        
    while(count < dic[staff][-1][0]):
        while(count < dic[staff][begin][0]):
            if dic[staff][begin][1] == 0:
                chord_gogo.append(set())
            else:
                now = [pit%12 for pit in dic[staff][begin][1:]]
                if len(now)>1:
                    chord_gogo.append(set(now))
                else:
                    chord_gogo.append(set())
            count += 1.0/2 
        begin += 1
    chord_dic.update({staff : chord_gogo})

all_chord =  tuple(chord_dic.values())
combined = map(lambda *args: reduce(lambda x,y: x|y,args),*all_chord)

final_chord = []
for a in combined:
    if list(a) == []:
        final_chord.append(0)
    else:
        closest = nearest(chord_np,convert(tuple(a)))
        final_chord.append(chord[tuple(closest)])
final_chord = [str(a) for a in final_chord]
fout = open(base_addr+musicname.split('.')[0]+'.txt','w')
fout.write(','.join(final_chord))
fout.close()