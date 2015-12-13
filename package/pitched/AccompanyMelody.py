from decimal import *

chord = {
    'C':(0, 4, 7),
	'C7':(0,4,7,10),
    'Cmaj7':(0, 4, 7, 11),
    'Dm':(2, 5, 9),
	'D':(2,6,9),
    'Dm7':(2, 5, 9, 12),
	'D7':(2,6,9,12),
	'E':(4,8,11),
	'E7':(4,8,11,14),
    'Em':(4, 7, 11),
    'Em7':(4, 7, 11, 14),
    'F':(5, 9, 12),
    'Fmaj7':(5, 9, 12, 16),
    'G':(7, 11, 14),
    'G7':(7, 11, 14, 17),
	'A':(9,13,16),
    'Am':(9, 12, 16),
    'Am7':(9, 12, 16, 19),
    'Bb':(10, 14, 17),
    'Bdim':(11, 14, 17)
}
def varChord(curChord):
	randomInt = 0
	#randomInt = randint(0,5)
	notes = ''
	for i, component in enumerate(chord[curChord], 1):
		if (randomInt == 1 and i == 1) or (randomInt == 2 and (i == 1 or i == 2)) or randomInt == 3:
			component += 12
		elif randomInt == 4 or (randomInt == 5 and ((len(chord[curChord]) == 3 and i == 3) or (len(chord[curChord]) == 4 and i == 4))):
			component -= 12
		component += 60
		notes += str(component) + ','
	return notes[:-1] + ';'
	
def nextChord(beatSum, indexAcc,chordProg):
    indexAcc += 1
    curChord = chordProg[indexAcc]
    diff = beatSum - Decimal(0.5)
    if diff >= 0.5:
        beatSum, indexAcc, curChord = nextChord(diff, indexAcc)
    else:
        beatSum = diff
    return beatSum, indexAcc, curChord

def accompanyMelody(measure, chordProg):
	staffReturn = {}
	for key in sorted(measure.keys()):
		indexAcc = 0
		curChord = chordProg[indexAcc]
		beatSum = 0
		re = ''
		totalBeatSum = 0
		for beat in measure[key].split(';'):
			duration = beat.split(',')[0]
			noteSign = beat.split(',')[1]
			#Determine when to select next chord
			if beatSum >= 0.5:
				beatSum, indexAcc, curChord = nextChord(beatSum, indexAcc,chordProg)

			#Generate different strings according to if it's a note or a rest
			if noteSign == '1' and curChord != '0':
				re += duration + ',' + varChord(curChord)
			else:
				re += duration + ',0;'

			#Add 0.0000000000001 to beatSum while it's a tuplet note
			if Decimal(duration) * 128 % 1 == 0:
				beatSum += Decimal(duration)
			else:
				beatSum += Decimal(duration) + Decimal(0.000000001)

		staffReturn[key] = re[:-1]
	return staffReturn
