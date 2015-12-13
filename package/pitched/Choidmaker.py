from bs4 import BeautifulSoup as bs
from decimal import *
import re
def Choidmaker (testkey):
    BDic = {Decimal('0.03125'): '32nd', Decimal('0.25'): 'quarter',Decimal('0.5'): 'half', Decimal('1'): 'whole', Decimal('0.00390625'): '256th', Decimal('0.015625'): '64th',None: 'measure', Decimal('0.0625'): '16th', Decimal('0.125'): 'eighth', Decimal('0.0078125'): '128th'}
    stafflist = map(lambda x :x.keys()[0],testkey)
    stafflist = list(set(stafflist))
    timesigN = 4
    Division = 480
    idtag=0
    newM = bs('')
    for stfno in range(0,len(stafflist)):
        a = filter(lambda a : a if a.keys()[0] in stafflist[stfno] else None ,testkey)
        no = re.match('.*?(\d+)',stafflist[stfno]).group(1)
        newM.append(newM.new_tag('Staff',id = no))
        mes=bs('');i=1;
        for x in a:
            bag =bs('')
            mes.append(mes.new_tag('Measure',number = str(i)))
            s = x[stafflist[stfno]].copy()
            tkno =0
            tkvalue = s.pop('track0')

            bag.append(ChoidUnit(tkno,tkvalue,idtag)[0])
            idtag+=1
            if len(s) > 0:
                tick = bag.new_tag('tick')
                tick.string= str(Division*timesigN*(i-1))
                bag.append(tick)
            for track in s.keys():
                tkno = int(track.split('k')[-1])
                tkvalue = x[stafflist[stfno]][track]
                bag.append(ChoidUnit(tkno,tkvalue,idtag)[0])
                idtag+=1
            mes.select('Measure')[i-1].append(bag)
            i += 1           
        newM.select('Staff')[stfno].append(mes)
    return newM
def ChoidUnit(tkno,tkvalue,idtag):
    BDic = {Decimal('0.03125'): '32nd', Decimal('0.25'): 'quarter',Decimal('0.5'): 'half', Decimal('1'): 'whole', Decimal('0.00390625'): '256th', Decimal('0.015625'): '64th',None: 'measure', Decimal('0.0625'): '16th', Decimal('0.125'): 'eighth', Decimal('0.0078125'): '128th'}
    sigN=4;sigD=4;Ts = sigN/sigD
    bag =[];Mli=[]
    tupletlist = [0,0,0,Decimal(3)/2,0,Decimal(5)/4,0,Decimal(7)/8,0,Decimal(9)/8]
    for durationtime in tkvalue.split(';'):
        dt = durationtime.split(',').pop(0);
        dt = Decimal(dt)
        p = durationtime.split(',')[1:]
        if [x for x in tupletlist if dt*x in BDic]:
            T = [x for x in tupletlist if dt*x in BDic]
            tupletTag = tupletlist.index(T[0]);Bbeat = T[0]*dt
        else :
            tupletTag = 0;Bbeat =dt
        bag.append(Bbeat)
        splitMeasure(Mli,bag,tupletTag,p)
    bag=[];Measure=[[]];i=0
    for s in Mli:
        bag.append(s.keys()[0])
        Measure[i].append(s)
        if sum(bag) == Ts:
            i+=1
            bag=[]
            Measure.append([])
    Measure.pop()
    addB =[[]]
    for i in range(0,len(Measure)):
        AA = Measure[i]
        for Bitem in range(0,len(AA)):
            R = AA[Bitem].keys()[0]
            l =AA[Bitem][R][0]; m =AA[Bitem][R][1]
            addB[i].append([l,R,0,m])
        addB.append([])
    addB.pop()
    Ilist=[];bag=[];tupbag=[];Tag=[];i=0
    for AA in addB:
        for c in range(0,len(AA)):
            if AA[c][3] > 0 :
                bag.append(AA[c][1])
                Ilist.append(c)
                if sum(bag)/AA[c][3] in BDic:
                    tupbag.append(i)
                    tupbag.extend(Ilist)
                    tupbag.insert(0,[BDic[sum(bag)/AA[c][3]],AA[c][3]])
                    Tag.append(tupbag)
                    bag =[];tupbag=[];Ilist=[]
        i+=1
    bag = [[]]
    for i in range(0,len(Tag)):
        T = Tag[i];no=0
        for s in T[2:]:
            bag[i].append([T[0][0],T[0][1],no])
            no+=1
        bag.append([])
        n =0
        for r in T[2:]:
            addB[T[1]][r][-1] = bag[i][n]
            n +=1
    Measure = addB

    addB =[[]]
    dotslist =[Decimal(2)/3,Decimal(4)/7,Decimal(8)/15] 
    for i in range(0,len(Measure)):
        AA = Measure[i]
        for Bitem in AA:
            R = Bitem[1]
            l = Bitem[0]; 
            m =Bitem[3]
            if R in BDic:
                dot = 0
                addB[i].append([l,BDic[R],dot,m])
            elif [x for x in [Decimal(2)/3,Decimal(4)/7,Decimal(8)/15] if R*x in BDic]:
                DD =  [x for x in dotslist if R*x in BDic]
                dot = dotslist.index(DD[0])+1
                addB[i].append([l,BDic[DD[0]*R],dot,m])
        addB.append([])
    addB.pop()
    New = bs('')
    
    for a in addB[i]:
        if tkno == 0:
            if a[3]!=0:
                if a[3][2] ==0:
                    New.append(Choid(0,a).BeautifulTag(idtag))
                    idtag+=1
            else:
                New.append(Choid(0,a).BeautifulTag(None))
        elif tkno !=0:
            if a[3]!=0:
                if a[3][2] ==0:
                    New.append(Choid(0,a).BeautifulTag(idtag))
                    idtag += 1
            else:
                New.append(Choid(0,a).BeautifulTag(None))
    return New,idtag
def splitMeasure(Mli,bag,tupletTag,p):
    if sum(bag) == 1:
        A = bag.pop()
        Mli.append({A:(p,tupletTag)})
        return Mli
    elif sum(bag) > 1:
        least = sum(bag)-1
        A = bag.pop()
        Nk = A-least
        Mli.append({Nk:(p,tupletTag)})
        bag = []
        bag.append(least)
        return splitMeasure(Mli,bag,tupletTag,p)
    elif sum(bag) < 1 :
        Mli.append({bag[-1]:(p,tupletTag)})
        return Mli
class Choid:
    
    def __init__(self,trackno,ChoidParameters,velocity=100):
        self.trackno = trackno
        self.ChoidParameters = ChoidParameters
        Choid.ispitchs = list(ChoidParameters[0])
        Choid.isduTime = ChoidParameters[1]
        Choid.isdots = ChoidParameters[2]
        Choid.isTuplet = ChoidParameters[3]
        self.velocity = velocity        
    
    def TupletTag(self,Tupletid,isTuplet,ChordTag):
        dic_normalNotes={3:2,5:4,7:8,9:8}
        dic_actualNotes={3:3,5:5,7:7,9:9}
        Tuplet = ChordTag.new_tag("Tuplet")
        Tuplet['id']= Tupletid
        Tuplet.string = "\n"
        ChordTag.append(Tuplet)
        Tuplet.insert_after(ChordTag.new_string("\n"))
        normalNotes = ChordTag.new_tag("normalNotes")
        normalNotes.string = str(dic_normalNotes[Choid.isTuplet[1]])
        Tuplet.append(normalNotes)
        normalNotes.insert_after(ChordTag.new_string("\n"))
        actualNotes = ChordTag.new_tag("actualNotes")
        actualNotes.string = str(dic_actualNotes[Choid.isTuplet[1]]) 
        Tuplet.append(actualNotes)
        actualNotes.insert_after(ChordTag.new_string("\n"))
        baseNote = ChordTag.new_tag("baseNote")
        baseNote.string = Choid.isTuplet[0]
        Tuplet.append(baseNote)
        baseNote.insert_after(ChordTag.new_string("\n"))
        Number = ChordTag.new_tag("Number")
        Number.string = "\n"
        Tuplet.append(Number)
        Number.insert_after(ChordTag.new_string("\n"))
        style = ChordTag.new_tag("style")
        style.string = "Tuplet"
        Number.append(style)
        style.insert_after(ChordTag.new_string("\n"))
        text = ChordTag.new_tag("text")
        text.string = str(Choid.isTuplet[1])
        Number.append(text)
        text.insert_after(ChordTag.new_string("\n"))        
    
    
    def BeautifulTag(self,idTag):
        Tupletid = idTag
        ChordTag = bs("")
        if Choid.ispitchs == str(0) and Choid.isduTime=='whole':
            ChordTag.append(TagR.new_tag("Rest"))
            if self.trackno > 0 :
                track = ChordTag.new_tag("track")
                track.string = str(Choid.trackno)
                ChordTag.Rest.append(track)
            durT = ChordTag.new_tag("durationType")
            durT.string = "measure"
            ChordTag.Rest.append(durT)
        elif Choid.ispitchs==str(0):
            Trest = ChordTag.append(ChordTag.new_tag("Rest"))
            if trackno > 0 :
                track = ChordTag.new_tag("track")
                track.string= str(Choid.trackno)
                ChordTag.Rest.append(track)
            durT = ChordTag.new_tag("durationType")
            durT.string = Choid.isduTime
            ChordTag.Rest.append(durT)
        else:
            if Choid.isTuplet!=0 and Choid.isTuplet[2]==0:
                dic_normalNotes={3:2,5:4,7:8,9:8}
                dic_actualNotes={3:3,5:5,7:7,9:9}
                Tuplet = ChordTag.new_tag("Tuplet")
                Tuplet['id']= Tupletid
                Tuplet.string = "\n"
                ChordTag.append(Tuplet)
                Tuplet.insert_after(ChordTag.new_string("\n"))
                normalNotes = ChordTag.new_tag("normalNotes")
                normalNotes.string = str(dic_normalNotes[Choid.isTuplet[1]])
                Tuplet.append(normalNotes)
                normalNotes.insert_after(ChordTag.new_string("\n"))
                actualNotes = ChordTag.new_tag("actualNotes")
                actualNotes.string = str(dic_actualNotes[Choid.isTuplet[1]]) 
                Tuplet.append(actualNotes)
                actualNotes.insert_after(ChordTag.new_string("\n"))
                baseNote = ChordTag.new_tag("baseNote")
                baseNote.string = Choid.isTuplet[0]
                Tuplet.append(baseNote)
                baseNote.insert_after(ChordTag.new_string("\n"))
                Number = ChordTag.new_tag("Number")
                Number.string = "\n"
                Tuplet.append(Number)
                Number.insert_after(ChordTag.new_string("\n"))
                style = ChordTag.new_tag("style")
                style.string = "Tuplet"
                Number.append(style)
                style.insert_after(ChordTag.new_string("\n"))
                text = ChordTag.new_tag("text")
                text.string = str(Choid.isTuplet[1])
                Number.append(text)
                text.insert_after(ChordTag.new_string("\n"))      
            Chord = ChordTag.new_tag("Chord")
            Chord.string = "\n"
            ChordTag.append(Chord)
            Chord.insert_after(ChordTag.new_string("\n"))
            if self.trackno > 0 :
                track = ChordTag.new_tag("track")
                track.string= str(self.trackno)
                ChordTag.Chord.append(track)
                track.insert_after(ChordTag.new_string("\n")) 
            if Choid.isdots >0:
                dots = ChordTag.new_tag("dots")
                dots.string = str(Choid.isdots)
                Chord.append(dots)
                dots.insert_after(ChordTag.new_string("\n"))  
            durationType = ChordTag.new_tag("durationType")
            durationType.string = Choid.isduTime
            Chord.append(durationType)
            durationType.insert_after(ChordTag.new_string("\n"))
            
            for i in range(0,len(Choid.ispitchs)):
                Note = ChordTag.new_tag("Note")
                Note.string = "\n"
                Chord.append(Note)
                Note.insert_after(ChordTag.new_string("\n"))
                Accidental = ChordTag.new_tag("Accidental")
                Accidental.string = "\n"
                Note.append(Accidental)
                Accidental.insert_after(ChordTag.new_string("\n"))
                subtype = ChordTag.new_tag("subtype")
                subtype.string = "sharp"
                Accidental.append(subtype)
                subtype.insert_after(ChordTag.new_string("\n"))
                pitch = ChordTag.new_tag("pitch")
                pitch.string = str(Choid.ispitchs[i])
                Note.append(pitch)
                pitch.insert_after(ChordTag.new_string("\n"))
                tpc = ChordTag.new_tag("tpc")
                tpc.string = "25"
                Note.append(tpc)
                tpc.insert_after(ChordTag.new_string("\n"))
                velo = ChordTag.new_tag("velocity")
                velo.string = str(self.velocity)
                Note.append(velo)
                velo.insert_after(ChordTag.new_string("\n"))
                veloType = ChordTag.new_tag("veloType")
                veloType.string = "user"
                Note.append(veloType)
                veloType.insert_after(ChordTag.new_string("\n"))
        return ChordTag
