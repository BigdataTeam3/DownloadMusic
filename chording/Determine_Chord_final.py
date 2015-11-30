import numpy as np
from decimal import *
import sys
import math

def convert(tu):
    if len(tu) != 12:
        origin = [0,0,0,0,0,0,0,0,0,0,0,0]
        for i in tu:
            origin[i%12]=1
        return tuple(origin)
    else:
        se = set()
        for i,n in enumerate(tu):
            if n == 1:
                se.add(i)
        return se
class Chord_class:
	@staticmethod
	def match(no,num=None):
		if num != None:
			for c in Chord_class.chord7:
				if set(convert(c))-set(no) == set():
					return Chord_class.chord[c]
			return None
		else:
			for c in Chord_class.chord:
				if set(no)-set(convert(c)) == set():
					return Chord_class.chord[c]
			return None
	chord7 = {(0,4,7,11):'Cmaj7',(0,2,5,9):'Dm7',(2,4,7,11):'Em7',(0,4,5,9):'Fmaj7',(2,5,7,11):'G7',(0,4,7,9):'Am7'}
	chord = {convert((0,4,7)):'C',convert((2,5,9)):'Dm',convert((4,7,11)):'Em',convert((0,5,9)):'F',convert((2,7,11)):'G',convert((0,4,9)):'Am',convert((2,5,10)):'Bb',convert((2,5,11)):'Bdim'}
	chord_np = np.array(chord.keys())
	key = {0:'C',2:'Dm',4:'Em',5:'F',7:'G',9:'Am',11:'Bdim'}

def nearest(nparray, pt):
	if len(pt) != 12:
		pt = convert(pt)
	n = [math.sqrt(sum((i-pt)**2)) for i in nparray]
	mindis = min(n)
	idx = n.index(mindis)
	return nparray[idx]

def determine_chord(ch):
	ch = set([p%12 for p in ch])
	if len(ch) == 0:
		return None
	if len(ch) >= 4:
		if Chord_class.match(ch,1):
			return Chord_class.match(ch,1)
		else:
			return Chord_class.chord[tuple(nearest(Chord_class.chord_np,ch))]
	if len(ch) == 3:
		return Chord_class.chord[tuple(nearest(Chord_class.chord_np,ch))]
	if len(ch) == 2:
		if Chord_class.match(ch):
			return Chord_class.match(ch)
		else:
			return None
	if len(ch) ==1:
		return None
	
def comb_chords(result_chords):
	sorted_chord = {}
	for staff in result_chords:
		sorted_chord.update({staff:[]})
		for time in sorted(result_chords[staff]):
			sorted_chord[staff].append((result_chords[staff][time]))
	t = tuple(sorted_chord.values())
	chord_more_than_1 = map(lambda *args: reduce(lambda x,y: x|y,filter(lambda l:len(l)>1,args)) if filter(lambda l:l is not None and len(l)>1,args) else set(),*t)
	chord_1 = map(lambda *args: reduce(lambda x,y: x|y,args),*t)
	return map(lambda x,y: x if len(x)>0 else y,chord_more_than_1,chord_1)

def final_determined(chord_combined):
	final_chord = []
	position = 0
	special_case = False
	buffer_notes = set()
	for ad,ch in enumerate(chord_combined):
		if ad%4 != 0 and special_case == False:
			continue
		elif ad%4 == 0:
			cc = determine_chord(ch)
			if cc is None:
				buffer_notes = set(ch)
				special_case = True
			else:
				final_chord.append(cc)
		else:
			buffer_notes = buffer_notes | set(ch)
			if ad%4 == 3:
				special_case = False
				if len(buffer_notes) == 0:
					final_chord.append(0)
				else:
					bcc = determine_chord(buffer_notes)
					note_mod = set([b%12 for b in buffer_notes])
					if bcc is None:
						if len(note_mod) == 1:
							final_chord.append(Chord_class.key[min(buffer_notes)%12])
						else:
							try:
								final_chord.append(Chord_class.key[min(buffer_notes)%12])
							except KeyError:
								final_chord.append('None')
					else:
						final_chord.append(bcc)
				buffer_notes = set()
	return final_chord