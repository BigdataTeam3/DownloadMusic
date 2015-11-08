
# coding: utf-8

# ## Determine main melody 
#  - by score (author specified)
#  - pan (左右聲道平衡度)
#  - velociy (按鍵力道)
#  - 平均旋律
#  - 和弦所佔比率

# In[2]:

main_name = ['melody','melodies','vocal','voice','sing','lead']
sub_name = ['drum']


# ## pan value

# In[3]:

def panDect(parts):
    pan = {}
    for part in parts:
        staffs = part.select('Staff')
        for staff in staffs:
            i = staff.get('id')
            channel = part.select('Channel')[0].select('controller')
            value = 0
            if len(channel) == 0 or len(channel.select('controller')) == 0 or channel.select('controller')[0].get('ctrl') != '10':
                value = 63
            else:
                value = channel.select('controller')[0].get('value')
            pan.update({i:value})
    return pan


# ## average velocity

# In[4]:

def velDect(addr,ids):
    fm = open(addr, 'r')
    music = fm.read()
    fm.close()
    vela = {}
    staffs = [staff for staff in bs(music,'xml').select('Score > Staff') if staff.get('id') in ids]
    for staff in staffs:
        vels = staff.select('Note velocity')
        n = len(vels)
        s = 0.0
        for vel in vels:
            v = int(vel.text)
            s += v
        avg = s/n
        vela.update({staff.get('id'):str(avg)})
    return vela


# ## average pitch

# In[5]:

import math
def pitDect(addr,ids):
    fm = open(addr, 'r')
    music = fm.read()
    fm.close()
    pits = {}
    dutype = {'whole':1.0,'half':1.0/2,'quarter':1.0/4,'eighth':1.0/8,'16th':1.0/16,'32nd':1.0/32,'64th':1.0/64,'128th':1.0/128}
    staffs = [staff for staff in bs(music,'xml').select('Score > Staff') if staff.get('id') in ids]
    for staff in staffs:
        pitch_sum = 0
        pitch_time = 0
        for measure in staff.select('Measure'):
            for chord in [c for c in list(measure.children) if c != '\n' and c.name == 'Chord']:
                max_pitch = max([int(d.pitch.text) for d in chord.select('Note')])
                dot = 0
                if len(chord.select('dot')) != 0:
                    dot = int(chord.select('dot')[0].text)
                dutime = dutype[chord.durationType.text] * (2-math.pow(1.0/2,dot))
                pitch_sum += max_pitch * dutime
                pitch_time += dutime
        avg_pich = pitch_sum/pitch_time
        pits.update({staff.get('id'):str(avg_pich)})
    return pits


# ## chords' rate

# In[6]:

def rateDect(addr,ids):
    fm = open(addr, 'r')
    music = fm.read()
    fm.close()
    rates = {}
    staffs = [staff for staff in bs(music,'xml').select('Score > Staff') if staff.get('id') in ids]
    for staff in staffs:
        num = 0
        n = 0
        for measure in staff.select('Measure'):
            chords = [c for c in list(measure.children) if c != '\n' and c.name == 'Chord']
            n += len(chords)
            for chord in chords:
                if len(chord.select('Note')) == 1:
                    num += 1
        rates.update({staff.get('id'):str(float(num)/n)})
    return rates


# ## sound area

# In[7]:

def areaDect(addr,ids):
    fm = open(addr, 'r')
    music = fm.read()
    fm.close()
    area = {}
    staffs = [staff for staff in bs(music,'xml').select('Score > Staff') if staff.get('id') in ids]
    dutype = {'whole':1.0,'half':1.0/2,'quarter':1.0/4,'eighth':1.0/8,'16th':1.0/16,'32nd':1.0/32,'64th':1.0/64,'128th':1.0/128}
    for staff in staffs:
        du = 0
        all_du = []
        for measure in staff.select('Measure'):
            chords = [c for c in list(measure.children) if c != '\n' and c.name == 'Chord']
            for chord in chords:
                all_du.append(dutype[chord.durationType.text])
        area.update({staff.get('id'):str(sum(all_du))})
    return area


# ## determine main melodies

# In[94]:

import pandas as pd
def detMain(data):
    form = pd.DataFrame(data).transpose()
    form.columns = ['vel_rate','pit_rate','cho_rate','area','staff']
    # need to add...
    return form       


# ## main function

# In[2]:

from bs4 import BeautifulSoup as bs

def melody(addr):
    fm = open(addr, 'r')
    music = fm.read()
    fm.close()
    cand = bs(music,'xml').select('Part')
    main_cand = []
    sub_cand = []
    for s in [par for par in cand if len(par.select('longName')) != 0]:
        pname = s.select('longName')[0].text.encode('utf8').lower()
        if len([word for word in main_name if word in pname]) != 0: # instru. name
            main_cand.append(s)
            cand.remove(s)
        if len([word for word in sub_name if word in pname]) != 0:
            sub_cand.append(s)
            cand.remove(s)
        for cin in [c for c in list(s.select('Instrument')[0].children) if c != '\n']: # more than one instru. in this staff
            if cin.get('pitch') is not None:
                if s in cand:
                    sub_cand.append(s)
                    cand.remove(s)
                break

    mesg = {}
    pan = panDect(cand)
    ids = pan.keys()
    vels = velDect(addr,ids)
    pits = pitDect(addr,ids)
    rates = rateDect(addr,ids)
    area = areaDect(addr,ids)

    [mesg.update({a:[float(vels[a]),float(pits[a]),float(rates[a]),float(area[a]),float(a)]}) for a in pan.keys()]
    dframe = detMain(mesg)

    avg = dframe.mean(axis=0) # 0:column ; 1:row
    avg = list(avg)
    avg.pop(4)
    avg.append(1)
    dframe = dframe/avg
    
    f2 = open('Maindata.csv','a')
    dframe.to_csv(f2, header=False, index=False)
    f2.close()
    return dframe



# In[ ]:



