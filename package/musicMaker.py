import re
import sys
import math
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
from pitched.AccompanyMelody import accompanyMelody_test as aM_test
from pitched.Choidmaker import Choidmaker as maker
from pitched.Instrument import Instrument
from pitched.guitar_decide import patternChosen as pch
from pitched.guitar_decide import getGuitarPattern as ggp
from pitched.give_guitar_pitch import Dong
from pitched.BassAdd import addBass


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
		self.chordPattern = None
	def determineChords(self,gramPatterns,seed=None):
		grams = ggr(gramPatterns,seed=seed)
		print 'Chosen gram : '+ str(grams)
		self.chordPattern = grams
		return grams
	def setChords(self,notations):
		self.chordPattern = notations

	
	def summary(self):
		for staff in self.staffContents:
			print staff+' :'
			print 'use instrument: '+self.staffContents[staff].instrument
			print 'used measures: '+str(self.staffContents[staff].measures)
			print '=========================================='
		
	
	def getMeasuresPerByNotations(self,notations,seed=None,start=0,total=None):
		nowTrack = max(self.usedStaffs)*4+1
		for k in range(0,start):
			notations.insert(0,'0')
		if total is not None:
			for k in range(0,total-len(notations)):
				notations.append('0')
		print 'notations length : ' + str(len(notations))
		patternDic = {}
		for notation in set(notations):
			getkey = notation[0]
			info = getP(getkey,seed=seed)
			patternDic.update({notation:info})
		tempdic = {}
		for notation in patternDic:
			tempdic.update({notation:{}})
			for i,track in enumerate(sorted(patternDic[notation])):
				if track == 'track0':
					tempdic[notation].update({'track0':patternDic[notation][track]})
				else:
					tempdic[notation].update({'track'+str(nowTrack+i-1):patternDic[notation][track]})
					self.usedTracks.add(nowTrack+i-1)
		print self.usedTracks
		return [MeasureObject(tempdic[key]) for key in notations] # a list of MeasureObjects
		
	def getGuitarPitByNotations(self,notations,type,ins_pattern='electric guitar',seed=None,start=0,total=None):
		nowTrack = max(self.usedStaffs)*4+1
		for k in range(0,start):
			notations.insert(0,'0')
		if total is not None:
			for k in range(0,total-len(notations)):
				notations.append('0')
		fixedInstdb = pch(ins_pattern)
		print fixedInstdb
		patternDic = ggp(fixedInstdb,notations,type,seed=seed)
		print patternDic
		tempdic = {}
		for notation in patternDic:
			tempdic.update({notation:{}})
			for i,track in enumerate(sorted(patternDic[notation])):
				if track == 'track0':
					tempdic[notation].update({'track0':patternDic[notation][track]})
				else:
					tempdic[notation].update({'track'+str(nowTrack+i-1):patternDic[notation][track]})
					self.usedTracks.add(nowTrack+i-1)
		print self.usedTracks
		rhymes = [MeasureObject(tempdic[key]) for key in notations]
		oneMeasureChords = map(lambda x,y:[x]+[y],self.chordPattern[::2],self.chordPattern[1::2])
		if 'single' in type.lower():
			preparedPatterns = map(lambda r,chords:MeasureObject(aM_test(r.content,chords)),rhymes,oneMeasureChords)
		else:
			preparedPatterns = map(lambda r,chords:MeasureObject(Dong(chords,r.content)),rhymes,oneMeasureChords)
		return preparedPatterns

	
	def getMeasuresPitByGrams(self,rhymes=None,start=0,end=None):
		nowTrack = max(self.usedStaffs)*4+1
		if self.chordPattern is None:
			print 'Please define chords first'
			return None
		chords = self.chordPattern
		end = len(chords)
		print chords
		genPattern = []
		for k in range(0,len(chords)):
			if k<start:
				genPattern.append('0')
			elif k>=start and k<=end:
				genPattern.append(chords[k])
			else:
				genPattern.append('0')
		if rhymes:
			if len(rhymes)*2 != len(genPattern):
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
						self.usedTracks.add(int(nowTrack+i-1))
				modified_list.append(tempdic)
			oneMeasureChords = map(lambda x,y:[x]+[y],genPattern[::2],genPattern[1::2])
			preparedPatterns = map(lambda measure,chords:MeasureObject(aM(measure,chords)),modified_list,oneMeasureChords)
		else:
			pass # choose rhymes from db
		print self.usedTracks
		return preparedPatterns
		
	def addLongStaffByChords(self,instrument,match=None):
		chords = self.chordPattern
		oneMeasureChords = map(lambda x,y:[x]+[y],chords[::2],chords[1::2])
		if match:
			oneMeasureChords = map(lambda m,chord:chord if m == '0' else ['0','0'],match,oneMeasureChords)
		mclist = []
		for chord in oneMeasureChords:
			if chord[0]==chord[1]:
				mclist.append(MeasureObject(aM({'track0':'1,1'},chord)))
			else:
				mclist.append(MeasureObject(aM({'track0':'0.5,1;0.5,1'},chord)))
		self.addStaff(mclist,instrument)
		
	def addStaff(self,mclist,instrument,velo=100,solo=False,staffid=None):
		if staffid is not None and staffid in self.usedStaffs:
			print 'Staff id in use.'
			return None
		else:
			staffid = max(self.usedStaffs)+1
			self.usedStaffs.add(staffid)
			num = len([mc.content for mc in mclist])
			if instrument == 'percussionType' and solo==False:
				velo=65
				tmplistc = []
				for mc in mclist:
					tmplistc.append({'staff'+str(staffid):mc.content})
				sta = StaffObject(num_of_measures=num,instrument=instrument,content=pc(tmplistc,velo))
				self.staffContents.update({'staff'+str(staffid):sta})
				
				staffid += 1
				self.usedStaffs.add(staffid)
				bass_list = []
				for measure in mclist:
					tmpdic = dict()
					c = measure.content
					for track in c:
						newstr = re.sub(',\d+',',0',re.sub(',36',',a',re.sub(',35',',a',c[track])))
						if 'a' in newstr:
							tmpdic.update({'track0':re.sub('a','1',newstr)})
					if len(tmpdic) == 0:
						bass_list.append({'track0':'1,0'})
					else:
						bass_list.append(tmpdic)
				oneMeasureChords = map(lambda x,y:[x]+[y],self.chordPattern[::2],self.chordPattern[1::2])

				pps = map(lambda measure,chords:MeasureObject(addBass(measure,chords)),bass_list,oneMeasureChords)				
				tmplistc = []
				for mc in pps:
					tmplistc.append({'staff'+str(staffid):mc.content})
				sta = StaffObject(num_of_measures=num,instrument='0',content=pc(tmplistc,velo))
				self.staffContents.update({'staff'+str(staffid):sta})
				print 'Autometically add staff'+str(staffid)+': Bass'
				
			elif instrument == 'percussionType' and solo==True:
				tmplistc = []
				for mc in mclist:
					tmplistc.append({'staff'+str(staffid):mc.content})
				sta = StaffObject(num_of_measures=num,instrument=instrument,content=pc(tmplistc,velo))
				self.staffContents.update({'staff'+str(staffid):sta})
				
			else:
				tmplistc = []
				for mc in mclist:
					tmplistc.append({'staff'+str(staffid):mc.content})
				sta = StaffObject(num_of_measures=num,instrument=Instrument.getInstrumentId(instrument),content=maker(tmplistc))
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
		