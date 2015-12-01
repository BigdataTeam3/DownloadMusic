from bs4 import BeautifulSoup as bs
from chording.chord_main import findChords as fc
from percussion.extract_percussion import return_pattern as rp
from algo.N_gram import N_gram_main_function_multiple as ngram
from algo.Association import asso_main as am
import re

class Music:
	def __init__(self,addr,main_melody=None):
		with open(addr,'r') as f:
			mscx = bs(f.read(),'xml')
		self.music = mscx
		self.main_melody = main_melody

	def getChords(self):
		return fc(self.music,self.main_melody)
		
	def getPercussions(self):
		pers = rp(self.music)
		l = []
		for staff in pers:
			l.append(PercussionStaff(staff,pers[staff]))
		return l
	
	def getGram(self,pattern,num,com):
		return ngram(pattern,num,com)

class Staff:
	def __init__(self,stid,content):
		self.id = re.match('.*?(\d+)',stid).group(1)
		self.content = content
	def id(self):
		return self.id
	def content(self):
		return self.content

		
class PercussionStaff(Staff):
	def __init__(self,stid,content,sep_1=0.2,sep_2=0.07):
		Staff.__init__(self,stid,content)
		self.pattern,self.patternDetail = am(self.content,sep_1,sep_2)
	
	def pattern(self):
		return self.pattern
	def patternDetail(self):
		return self.patternDetail
		
	def resetSep(self,sep_1,sep_2):
		self.pattern,self.patternDetail = am(self.content,sep_1,sep_2)