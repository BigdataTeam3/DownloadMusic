from decimal import *

chord = {
    'C':[0],
	'C7':[0],
    'Cmaj7':[0],
    'Dm':[2],
	'D':[2],
    'Dm7':[2],
	'D7':[2],
	'E':[4],
	'E7':[4],
    'Em':[4],
    'Em7':[4],
    'F':[5],
    'Fmaj7':[5],
    'G':[7],
    'G7':[7],
	'A':[9],
    'Am':[9],
    'Am7':[9],
    'Bb':[10],
    'Bdim':[11]
}
def nextChord(beatSum, indexAcc, curChord,chordProg):
    indexAcc += 1
    curChord = chordProg[indexAcc]
    diff = beatSum-Decimal(0.5)
    if diff >= 0.5:
        beatSum, indexAcc, curChord = nextChord(diff, indexAcc, curChord)
    else:
        beatSum = diff
    return beatSum, indexAcc, curChord

def addBass(measure, chordProg):
	staffReturn = {}
	for key in sorted(measure.keys()):
		indexAcc = 0
		curChord = chordProg[indexAcc]
		beatSum = 0
		re = ''
		totalBeatSum = 0
		for beat in measure[key].split(';'):
			duration = beat.split(',')[0]
			noteOrRest = beat.split(',')[1]

			#Determine when to select next chord
			if beatSum >= 0.5:
				beatSum, indexAcc, curChord = nextChord(beatSum, indexAcc, curChord,chordProg)

			#Generate different strings according to note or rest
			if noteOrRest == '1':
				re += duration + ','
				C = 36
				for component in chord[curChord]:
					re += str(C+component) + ','
				re = re[:-1] + ';'
			else:
				re += duration + ',0;'

			#Add 0.0000000000001 to beatSum while it's a tuplet beat
			if Decimal(duration) * 128 % 1 == 0:
				beatSum += Decimal(duration)
			else:
				beatSum += Decimal(duration) + Decimal(0.0000000000001)

		staffReturn[key] = re[:-1]
	return staffReturn