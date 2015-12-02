
# coding: utf-8

# In[8]:

from bs4 import BeautifulSoup as bs
from decimal import *
BDic = {Decimal('0.03125'): '32nd', Decimal('0.25'): 'quarter',
        Decimal('0.5'): 'half', Decimal('1'): 'whole', Decimal('0.00390625'): '256th', Decimal('0.015625'): '64th',
        None: 'measure', Decimal('0.0625'): '16th', Decimal('0.125'): 'eighth', Decimal('0.0078125'): '128th'}


# #  只能給 打擊樂的staff !!
# data type : testkey = [{u'staff1': {u'track1': '0.25,44,36;0.25,44,36;0.25,44;0.25,44,36', 'track0': '0.5,0;0.25,38;0.25,0'}},
#                        {u'staff1': {u'track1': '0.25,70,66;0.25,72,56;0.25,44;0.25,60,86', 'track0': '0.5,0;0.25,38;0.25,0'}},
#                        {u'staff1': {u'track1': '0.25,44,36;0.25,44,36;0.25,44;0.25,44,36', 'track0': '0.5,0;0.25,38;0.25,0'}}]

# In[11]:

def Percussion (testkey):
    stafflist = map(lambda x :x.keys()[0],testkey)
    stafflist = list(set(stafflist))
    timesigN = 4
    Division = 480
    newM = bs('')
    for stfno in range(0,len(stafflist)):
        a = filter(lambda a : a if a.keys()[0] in stafflist[stfno] else None ,testkey)
        no = stafflist[stfno].split('ff')[-1]
        newM.append(newM.new_tag('Staff',id = no))
        mes=bs('');i=1
        for x in a:
            bag =bs('')
            mes.append(mes.new_tag('Measure',number = str(i)))
            s = x[stafflist[stfno]]
            tkno =0                               # track number = tkno
            tkvalue = s.pop('track0')
            bag.append(PercussionUnit(tkno,tkvalue))
            if len(s) > 0:
                tick = bag.new_tag('tick')       # 建構Division tag
                tick.string= str(Division*timesigN*(i-1))               # Division 480 * timesigN * measure number
                bag.append(tick)
            for track in s.keys():
                tkno = int(track.split('k')[-1])
                tkvalue = x[stafflist[stfno]][track]
                bag.append(PercussionUnit(tkno,tkvalue))
            mes.select('Measure')[i-1].append(bag)
            i += 1
        newM.select('Staff')[stfno].append(mes)
    return newM


# In[12]:

def PercussionUnit(tkno,tkvalue):
    Measure = [] ; Mli = [];a=[]
    for tkc in  tkvalue.split(';'):
        b = tkc.split(',').pop(0)
        p = tkc.split(',')[1:]
        Measure.append(b)
        Mli.append(p)

    b = Decimal(b)
    addB =[];dotslist = [Decimal(2)/3,Decimal(4)/7,Decimal(8)/15]
    for i in range(0,len(Measure)):
        Bitem = Measure[i]
        R = Decimal(Bitem)
        if R in BDic:
            dot = 0
            addB.append([Mli[i],BDic[R],dot])
        elif [x for x in dotslist if R*x in BDic]:
            DD =  [x for x in dotslist if R*x in BDic]
            dot = dotslist.index(DD[0])+1
            addB.append([Mli[i],BDic[DD[0]*R],dot])
    New = bs('')
    for a in range(0,len(addB)):
        if tkno == 0:
            New.append(Tchord(tkno,addB[a]))
        elif tkno !=0:
            New.append(Tchord(tkno,addB[a]))
    return New
        


# In[13]:

def Tchord(tkno,x):
    ccc = bs("")
    if (x[0][0] == str(0) and x[1]=='whole'):
        TagR = bs("")
        TagR.append(TagR.new_tag("Rest"))
        if tkno > 0 :
            track = TagR.new_tag("track")
            track.string= str(tkno)
            TagR.Rest.append(track)
        durT = TagR.new_tag("durationType")
        durT.string = "measure"
        TagR.Rest.append(durT)
        ccc.append(TagR)
    elif x[0][0]== str(0):
        Rtag = bs("")
        Trest = Rtag.append(Rtag.new_tag("Rest"))
        if tkno > 0 :
            track = Rtag.new_tag("track")
            track.string= str(tkno)
            Rtag.Rest.append(track)
        durT = Rtag.new_tag("durationType")
        durT.string = x[1]
        Rtag.Rest.append(durT)
        ccc.append(Rtag)
    else:
        Ctag = bs("")
        Tcho = Ctag.append(Ctag.new_tag("Chord"))
        if tkno > 0 :
            track = Ctag.new_tag("track")
            track.string= str(tkno)
            Ctag.Chord.append(track)
            ccc.append(Ctag)
        if x[2] >0:
            Tdot = Ctag.new_tag("dots")
            Tdot.string = str(x[2])
            Ctag.Chord.append(Tdot)
            durT = Ctag.new_tag("durationType")
            durT.string = x[1]
            Ctag.Chord.append(durT)
            ccc.append(Ctag)
        for i in range(0,len(x[0])):
            Tnote = Ctag.Chord.append(Ctag.new_tag("Note"))
            if tkno > 0 :
                track = Ctag.new_tag("track")
                track.string= str(tkno)
                Ctag.Chord.select('Note')[i].append(track)
            Tpitch = Ctag.new_tag("pitch")
            Tpitch.string= str(x[0][i])
            Ctag.select('Note')[i].append(Tpitch)
            Ttpc = Ctag.new_tag("tpc")
            Ttpc.string="22"
            Ctag.select('Note')[i].append(Ttpc)
            Tvelo = Ctag.new_tag("velocity")
            Tvelo.string="100"
            Ctag.select('Note')[i].append(Tvelo)
            TvT = Ctag.new_tag("veloType")
            TvT.string="user"
            Ctag.select('Note')[i].append(TvT)
            ccc.append(Ctag)
    return ccc


# In[ ]:



