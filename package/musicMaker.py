import re
import sys
from bs4 import BeautifulSoup as bs
from chording.chord_main import *
from percussion.extract_percussion import return_pattern as rp
from percussion.Composer import Percussion as pc
from algo.N_gram import N_gram_main_function_multiple as ngram
from algo.Association_analysis import asso_main as am
from algo.Association_analysis import Get_percussion_from_mongodb as getP
from algo.Taking_Grams import getGrams as ggr
from algo.CombineToSheet import staffToSheet
from pitched.AccompanyMelody import accompanyMelody as aM

class Music:
	def __init__(self,addr,main_melody=None):
		with open(addr,'r') as f:
			mscx = bs(f.read(),'xml')
		self.music = mscx
		self.main_melody = main_melody

	def getChords(self):
		return findChords(self.music,self.main_melody)
		
	def getPichedStaffs(self):
		l = []
		fst = findStaffInfo(self.music)
		for staff in fst:
			l.append(PitchedStaff(staff,fst[staff]['content'],fst[staff]['instrument']))
		return l
		
	def getPercussions(self):
		pers = rp(self.music)
		l = []
		for staff in pers:
			l.append(PercussionStaff(staff,pers[staff]))
		return l
	
	def getGram(self,pattern,num,com):
		return ngram(pattern,num,com)

class MusicCreator:
	def __init__(self):
		self.usedStaffs = set([0])
		self.usedTracks = set([0])
		self.staffContents = dict()
	
	def getMeasuresPerByNotations(self,notations,seed=None,start=0,total=None):
		nowTrack = max(self.usedTracks)+1
		for k in range(0,start):
			notations.insert(0,'0')
		if total is not None:
			for k in range(0,total-len(notations)):
				notations.append('0')
		print 'notations length : ' + str(len(notations))
		patternDic = {}
		for notation in set(notations):
			getkey = notation[0]
			info = getP(getkey,seed)
			patternDic.update({notation:info})
		tempdic = {}
		for notation in patternDic:
			tempdic.update({notation:{}})
			for i,track in enumerate(sorted(patternDic[notation])):
				if track == 'track0':
					tempdic[notation].update({'track0':patternDic[notation][track]})
				else:
					tempdic[notation].update({'track'+str(nowTrack+i-1):patternDic[notation][track]})
				self.usedTracks.add(i)
		return [MeasureObject(tempdic[key]) for key in notations] # a list of MeasureObjects
	
	def getMeasuresPitByGrams(self,gramPatterns,seed=None,rhymes=None,start=0,total=None):
		nowTrack = max(self.usedTracks)+1
		for k in range(0,start):
			gramPatterns.insert(0,'0')
		if total is not None:
			for k in range(0,total-len(notations)):
				gramPatterns.append('0')
		grams = ggr(gramPatterns)
		print 'Chosen gram : '+ str(grams)
		if rhymes:
			if len(rhymes)*2 != len(grams):
				print 'Wrong length..'
				return None
			modified_list = []
			for rhyme in rhymes:
				tempdic = dict()
				for i,track in enumerate(sorted(rhyme)):
					if track == 'track0':
						tempdic.update({'track0':rhyme[track]})
					else:
						tempdic.update({'track'+str(nowTrack+i-1):rhyme[track]})
					self.usedTracks.add(i)
				modified_list.append(tempdic)
			oneMeasureChords = map(lambda x,y:[x]+[y],grams[::2],grams[1::2])
			preparedPatterns = map(lambda measure,chords:MeasureObject(aM(measure,chords)),modified_list,oneMeasureChords)
		else:
			pass # chosen rhymes from db
		return preparedPatterns
		
		
	def getMeasuresPitByChords(self,chords,rhymes=None):
		nowTrack = max(self.usedTracks)+1
		whole_list = []
		for num,chord in enumerate(map(lambda x,y:[x,y],chords[::2],chords[1::2])): # 2 chords = 1 measure
			tempdic = {}
			if rhymes is not None:
				if len(rhymes) != len(chords)/2:
					print 'chords and rhymes mismatched!'
					return None
				else:
					pitched = aM(rhymes[num],list(chord))
			else:
				pass# add chosen rhyme codes here
			for i,track in enumerate(pitched):
				if track == 'track0':
					tempdic.update({'track0':pitched[track]})
				else:
					tempdic.update({'track'+str(nowTrack+i):pitched[track]})
				self.usedTracks.add(i)
			whole_list.append(MeasureObject(tempdic))
		return whole_list
	
	def addStaff(self,mclist,instrument,staffid=None):
		if staffid is not None and staffid in self.usedStaffs:
			print 'Staff id in use.'
			return None
		else:
			staffid = max(self.usedStaffs)+1
			self.usedStaffs.add(staffid)
			num = len([mc.content for mc in mclist])
			if instrument == 'percussionType':
				tmplistc = []
				for mc in mclist:
					tmplistc.append({'staff'+str(staffid):mc.content})
				sta = StaffObject(num_of_measures=num,instrument=instrument,content=pc(tmplistc))
				self.staffContents.update({'staff'+str(staffid):sta})
			else:
				tmplistc = []
				for mc in mclist:
					tmplistc.append({'staff'+str(staffid):mc.content})
				sta = StaffObject(num_of_measures=num,instrument=instrument,content=pc(tmplistc))
				self.staffContents.update({'staff'+str(staffid):sta})

	def createSheet(self):
		return staffToSheet(self.staffContents)
		
				

class Staff:
	def __init__(self,stid,content):
		self.id = re.match('.*?(\d+)',stid).group(1)
		self.content = content
	
	def joinByMeasure(self):
		m_dic = {}
		for measure in self.content:
			m_num = int(re.match('.*?(\d+)',measure).group(1))
			m_dic.update({m_num:self.content[measure]})
		returned_dic = {}
		for num in sorted(m_dic):
			for track in m_dic[num]:
				if returned_dic.get(track) is None:
					returned_dic.update({track:m_dic[num][track]})
				else:
					returned_dic[track] += ';'+m_dic[num][track]
		return returned_dic

		
class PercussionStaff(Staff):
	def __init__(self,stid,content,sep_1=0.2,sep_2=0.07):
		Staff.__init__(self,stid,content)
		self.pattern,self.patternDetail = am(self.content,sep_1,sep_2)
		self.instrument = 'percussionType'
		
	def resetSep(self,sep_1,sep_2):
		self.pattern,self.patternDetail = am(self.content,sep_1,sep_2)
		
class PitchedStaff(Staff):
	def __init__(self,stid,content,instrument):
		Staff.__init__(self,stid,content)
		self.instrument = instrument

class MusicObject:
	def __init__(self,division=480,tempo=120,timesig='4/4'):
		self.division = division
		self.tempo = tempo
		self.timesig = timesig
		self.contentList = {}
		self.instrumentList = {}
	def addStaff(self,staffObject,staffid):
		self.contentlist.update({staffid:staffObject.content})
		self.instrumentList.update({staffid:staffObject.instrument})
		
	
class StaffObject:
	def __init__(self,num_of_measures=None,instrument=None,content=None):
		self.instrument = instrument
		self.measures = num_of_measures
		self.content = content
	def setNumOfMeasures(self,num_of_measures):
		self.measures = num_of_measures
	def setContent(self,content):
		self.content = content
	def setInstrument(self,instrument):
		self.instrument = instrument

class MeasureObject:
	def __init__(self,content):
		self.content = content
		