import re

class Instrument:
	@staticmethod
	def getInstrumentId(check):
		if re.match('\d',check) and int(check)>-1 and int(check)<128:
			return check
		name = check.lower()
		instrudic = {'Electric Guitar (jazz)': '26', 'Electric Bass (finger)': '33', \
		'Synth Bass 2': '39', 'Synth Bass 1': '38', 'Accordion': '21', 'Electric Grand Piano': '2', \
		'Bag pipe': '109', 'Timpani': '47', 'Tuba': '58', 'Tremolo Strings': '44', 'Harpsichord': '6', \
		'Bright Acoustic Piano': '1', 'Electric Piano 2': '5', 'Recorder': '74', 'Electric Piano 1': '4', \
		'Voice Oohs': '53', 'Drawbar Organ': '16', 'Melodic Tom': '117', 'Pizzicato Strings': '45', \
		'Pad 6 (metallic)': '93', 'Fiddle': '110', 'FX 1 (rain)': '96', 'Marimba': '12', \
		'Alto Sax': '65', 'FX 5 (brightness)': '100', 'Xylophone': '13', 'Steel Drums': '114', \
		'Church Organ': '19', 'Acoustic Bass': '32', 'Whistle': '78', 'Acoustic Guitar (steel)': '25', \
		'Taiko Drum': '116', 'Electric Guitar (muted)': '28', 'Shamisen': '106', 'Lead 1 (square)': '80', \
		'Baritone Sax': '67', 'Lead 5 (charang)': '84', 'SynthStrings 1': '50', 'FX 2 (soundtrack)': '97', \
		'Rock Organ': '18', 'Pad 8 (sweep)': '95', 'Orchestra Hit': '55', 'Shanai': '111', \
		'SynthStrings 2': '51', 'Woodblock': '115', 'SynthBrass 1': '62', 'Orchestral Harp': '46', \
		'SynthBrass 2': '63', 'Pad 4 (choir)': '91', 'Cello': '42', 'FX 3 (crystal)': '98', \
		'Lead 4 (chiff)': '83', 'Pad 3 (polysynth)': '90', 'Piccolo': '72', 'Music Box': '10', \
		'Choir Aahs': '52', 'FX 8 (sci-fi)': '103', 'Sitar': '104', 'Kalimba': '108', 'Seashore': '122', \
		'Honky-tonk Piano': '3', 'Clarinet': '71', 'Trumpet': '56', 'FX 7 (echoes)': '102', \
		'Telephone Ring': '124', 'FX 6 (goblins)': '101', 'Bassoon': '70', 'Tubular Bells': '14', \
		'English Horn': '69', 'Distortion Guitar': '30', 'Electric Bass (pick)': '34', \
		'Viola': '41', 'Synth Voice': '54', 'French Horn': '60', 'Pad 2 (warm)': '89', \
		'Pad 7 (halo)': '94', 'Tango Accordion': '23', 'Muted Trumpet': '59', 'Agogo': '113', \
		'Lead 7 (fifths)': '86', 'Synth Drum': '118', 'FX 4 (atmosphere)': '99', 'Oboe': '68', \
		'Lead 6 (voice)': '85', 'Shakuhachi': '77', 'Blown Bottle': '76', 'Flute': '73', \
		'Banjo': '105', 'Lead 2 (sawtooth)': '81', 'Tinkle Bell': '112', 'Percussive Organ': '17', \
		'Koto': '107', 'Pad 1 (new age)': '88', 'Guitar harmonics': '31', 'Fretless Bass': '35', \
		'Dulcimer': '15', 'Glockenspiel': '9', 'Overdriven Guitar': '29', 'Breath Noise': '121', \
		'Guitar Fret Noise': '120', 'Brass Section': '61', 'Acoustic Grand Piano': '0', \
		'Pan Flute': '75', 'Vibraphone': '11', 'Soprano Sax': '64', 'Clavi': '7', \
		'Contrabass': '43', 'Bird Tweet': '123', 'Violin': '40', 'Harmonica': '22', \
		'Slap Bass 1': '36', 'Slap Bass 2': '37', 'Lead 3 (calliope)': '82', \
		'Acoustic Guitar (nylon)': '24', 'Gunshot': '127', 'Electric Guitar (clean)': '27', \
		'Tenor Sax': '66', 'Helicopter': '125', 'Lead 8 (bass + lead)': '87', \
		'Celesta': '8', 'Pad 5 (bowed)': '92', 'Reverse Cymbal': '119', \
		'String Ensemble 1': '48', 'String Ensemble 2': '49', 'Trombone': '57', \
		'Reed Organ': '20', 'Ocarina': '79', 'Applause': '126',
		'piano':'0','guitar':'25','electric guitar':'30','percussionType':'percussionType'}
		for ins in instrudic:
			if name == ins.lower():
				return instrudic[ins]
		print 'Wrong instrument, use default Piano..'
		return '0'
			