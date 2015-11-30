from bs4 import BeautifulSoup as bs
from chording.chord_main import findChords as fc
from percussion.extract_percussion import return_pattern as rp

class Music:
	def __init__(self,addr,main_melody=None):
		with open(addr,'r') as f:
			mscx = bs(f.read(),'xml')
		self.music = mscx
		self.main_melody = main_melody

	def getChords(self):
		self.chords = fc(self.music,self.main_melody)
		return self.chords
		
	def getPercussions(self):
		self.percussion = rp(self.music)
		return self.percussion
	